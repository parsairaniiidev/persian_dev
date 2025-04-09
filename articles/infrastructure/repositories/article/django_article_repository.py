from django.db import transaction
from typing import List, Optional
from uuid import UUID
from domain.models.article import Article
from core.domain.models.user import User
from domain.value_objects.article_status import ArticleStatus
from application.interfaces.repositories.article_repository import ArticleRepository
from .models import DjangoArticle, DjangoArticleTag, DjangoArticleCategory

class DjangoArticleRepository(ArticleRepository):
    """پیاده‌سازی ریپازیتوری مقاله با استفاده از Django ORM"""
    
    def get_by_id(self, article_id: str) -> Optional[Article]:
        try:
            db_article = DjangoArticle.objects.get(id=article_id)
            return self._to_domain(db_article)
        except DjangoArticle.DoesNotExist:
            return None

    def get_by_slug(self, slug: str) -> Optional[Article]:
        try:
            db_article = DjangoArticle.objects.get(slug=slug)
            return self._to_domain(db_article)
        except DjangoArticle.DoesNotExist:
            return None

    @transaction.atomic
    def save(self, article: Article) -> Article:
        """ذخیره مقاله با مدیریت تراکنش"""
        tags = article.tags
        categories = article.categories
        
        # ایجاد یا به‌روزرسانی مقاله
        db_article, created = DjangoArticle.objects.update_or_create(
            id=article.id,
            defaults={
                'title': article.title,
                'slug': article.slug.value,
                'content': article.content,
                'author_id': article.author.id,
                'status': article.status.value,
                'published_at': article.published_at,
                'view_count': article.view_count
            }
        )
        
        # به‌روزرسانی تگ‌ها
        self._update_tags(db_article, tags)
        
        # به‌روزرسانی دسته‌بندی‌ها
        self._update_categories(db_article, categories)
        
        return self._to_domain(db_article)

    def _update_tags(self, db_article: DjangoArticle, tags: List[str]) -> None:
        """به‌روزرسانی تگ‌های مقاله"""
        current_tags = set(DjangoArticleTag.objects.filter(article=db_article)
                         .values_list('tag_name', flat=True))
        new_tags = set(tags)
        
        # حذف تگ‌های قدیمی
        DjangoArticleTag.objects.filter(
            article=db_article,
            tag_name__in=current_tags - new_tags
        ).delete()
        
        # اضافه کردن تگ‌های جدید
        tags_to_add = new_tags - current_tags
        DjangoArticleTag.objects.bulk_create([
            DjangoArticleTag(article=db_article, tag_name=tag)
            for tag in tags_to_add
        ])

    def _update_categories(self, db_article: DjangoArticle, categories: List[str]) -> None:
        """به‌روزرسانی دسته‌بندی‌های مقاله"""
        current_categories = set(DjangoArticleCategory.objects.filter(article=db_article)
                               .values_list('category_id', flat=True))
        new_categories = set(categories)
        
        # حذف دسته‌بندی‌های قدیمی
        DjangoArticleCategory.objects.filter(
            article=db_article,
            category_id__in=current_categories - new_categories
        ).delete()
        
        # اضافه کردن دسته‌بندی‌های جدید
        categories_to_add = new_categories - current_categories
        DjangoArticleCategory.objects.bulk_create([
            DjangoArticleCategory(article=db_article, category_id=cat_id)
            for cat_id in categories_to_add
        ])

    def _to_domain(self, db_article: DjangoArticle) -> Article:
        """تبدیل مدل دیتابیس به مدل دامنه"""
        from domain.models.article import Article
        from core.domain.models.user import User
        from domain.value_objects.slug import Slug
        
        return Article(
            title=db_article.title,
            content=db_article.content,
            author=User(
                id=db_article.author.id,
                username=db_article.author.username,
                # سایر ویژگی‌های کاربر
            ),
            tags=list(db_article.tags.values_list('tag_name', flat=True)),
            categories=list(db_article.categories.values_list('category_id', flat=True)),
            status=ArticleStatus(db_article.status),
            published_at=db_article.published_at,
            view_count=db_article.view_count
        )

    # سایر متدهای ریپازیتوری...