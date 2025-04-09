from typing import Optional
from dataclasses import dataclass
from articles.domain.value_objects.article_status import ArticleStatus
from domain.models.article import Article
from core.domain.models.user import User
from domain.exceptions.article_errors import (
    ArticleNotFoundError,
    ArticlePermissionError,
    ArticleValidationError
)
from application.interfaces.repositories.article_repository import ArticleRepository
from application.interfaces.services.search_service import SearchService

@dataclass
class UpdateArticleDTO:
    """شیء انتقال داده برای به‌روزرسانی مقاله"""
    article_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    editor: User  # کاربری که در حال ویرایش است

class UpdateArticleUseCase:
    """یوزکیس به‌روزرسانی مقاله"""
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        search_service: SearchService
    ):
        self.article_repository = article_repository
        self.search_service = search_service

    def execute(self, dto: UpdateArticleDTO) -> Article:
        """
        به‌روزرسانی مقاله با اعتبارسنجی و ذخیره تغییرات
        
        Args:
            dto: داده‌های مورد نیاز برای به‌روزرسانی
            
        Returns:
            Article: مقاله به‌روزرسانی شده
            
        Raises:
            ArticleNotFoundError: اگر مقاله یافت نشود
            ArticlePermissionError: اگر کاربر مجوز ویرایش نداشته باشد
            ArticleValidationError: اگر داده‌ها نامعتبر باشند
        """
        # یافتن مقاله
        article = self.article_repository.get_by_id(dto.article_id)
        if not article:
            raise ArticleNotFoundError(dto.article_id)
        
        # بررسی مجوز ویرایش
        if not self._can_edit(article, dto.editor):
            raise ArticlePermissionError(
                user_id=dto.editor.id,
                article_id=dto.article_id
            )
        
        # اعتبارسنجی داده‌های ورودی
        self._validate_input(dto)
        
        # اعمال تغییرات
        if dto.title is not None:
            article.title = dto.title
        
        if dto.content is not None:
            article.content = dto.content
        
        if dto.tags is not None:
            article.tags = dto.tags
        
        if dto.categories is not None:
            article.categories = dto.categories
        
        # ذخیره تغییرات
        updated_article = self.article_repository.save(article)
        
        # به‌روزرسانی اندکس جستجو
        if updated_article.status == ArticleStatus.PUBLISHED:
            self.search_service.update_indexed_article(updated_article)
        
        return updated_article

    def _can_edit(self, article: Article, editor: User) -> bool:
        """بررسی اینکه آیا کاربر مجوز ویرایش مقاله را دارد"""
        return (
            editor.is_admin or 
            editor.is_editor or 
            article.author.id == editor.id
        )

    def _validate_input(self, dto: UpdateArticleDTO) -> None:
        """اعتبارسنجی داده‌های ورودی"""
        if dto.title is not None and len(dto.title.strip()) < 10:
            raise ArticleValidationError(
                field_name="title",
                error_message="عنوان مقاله باید حداقل ۱۰ کاراکتر داشته باشد"
            )
            
        if dto.content is not None and len(dto.content.strip()) < 300:
            raise ArticleValidationError(
                field_name="content",
                error_message="محتوای مقاله باید حداقل ۳۰۰ کاراکتر داشته باشد"
            )