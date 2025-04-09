from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from domain.models.article import Article
from core.domain.models.user import User
from domain.value_objects.article_status import ArticleStatus
from domain.exceptions.article_errors import (
    ArticleValidationError,
    ArticleTitleDuplicateError
)
from application.interfaces.repositories.article_repository import ArticleRepository
from application.interfaces.services.search_service import SearchService

@dataclass
class CreateArticleDTO:
    """شیء انتقال داده برای ایجاد مقاله"""
    title: str
    content: str
    author: User
    tags: Optional[list[str]] = None
    categories: Optional[list[str]] = None
    status: Optional[ArticleStatus] = ArticleStatus.DRAFT

class CreateArticleUseCase:
    """یوزکیس ایجاد مقاله جدید"""
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        search_service: SearchService
    ):
        self.article_repository = article_repository
        self.search_service = search_service

    def execute(self, dto: CreateArticleDTO) -> Article:
        """
        ایجاد مقاله جدید با اعتبارسنجی و ذخیره در سیستم
        
        Args:
            dto: داده‌های مورد نیاز برای ایجاد مقاله
            
        Returns:
            Article: مقاله ایجاد شده
            
        Raises:
            ArticleValidationError: اگر داده‌ها نامعتبر باشند
            ArticleTitleDuplicateError: اگر عنوان تکراری باشد
        """
        # اعتبارسنجی داده‌های ورودی
        self._validate_input(dto)
        
        # بررسی تکراری نبودن عنوان
        if self.article_repository.exists_by_title(dto.title):
            raise ArticleTitleDuplicateError(dto.title)
        
        # ایجاد موجودیت مقاله
        article = Article(
            title=dto.title,
            content=dto.content,
            author=dto.author,
            tags=dto.tags,
            categories=dto.categories,
            status=dto.status
        )
        
        # ذخیره مقاله
        saved_article = self.article_repository.save(article)
        
        # اندیس کردن مقاله در موتور جستجو
        if saved_article.status == ArticleStatus.PUBLISHED:
            self.search_service.index_article(saved_article)
        
        return saved_article

    def _validate_input(self, dto: CreateArticleDTO) -> None:
        """اعتبارسنجی داده‌های ورودی"""
        if not dto.title or len(dto.title.strip()) < 10:
            raise ArticleValidationError(
                field_name="title",
                error_message="عنوان مقاله باید حداقل ۱۰ کاراکتر داشته باشد"
            )
            
        if not dto.content or len(dto.content.strip()) < 300:
            raise ArticleValidationError(
                field_name="content",
                error_message="محتوای مقاله باید حداقل ۳۰۰ کاراکتر داشته باشد"
            )