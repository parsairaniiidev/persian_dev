from dataclasses import dataclass
from core.domain.models.user import User
from domain.models.article import Article
from domain.value_objects.article_status import ArticleStatus
from domain.exceptions.article_errors import (
    ArticleNotFoundError,
    ArticlePermissionError,
    InvalidArticleStatusError
)
from application.interfaces.repositories.article_repository import ArticleRepository
from application.interfaces.services.search_service import SearchService

@dataclass
class ArchiveArticleDTO:
    """شیء انتقال داده برای بایگانی مقاله"""
    article_id: str
    archiver: User  # کاربری که در حال بایگانی مقاله است

class ArchiveArticleUseCase:
    """یوزکیس بایگانی مقاله"""
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        search_service: SearchService
    ):
        self.article_repository = article_repository
        self.search_service = search_service

    def execute(self, dto: ArchiveArticleDTO) -> Article:
        """
        بایگانی مقاله با اعتبارسنجی و انجام عملیات مرتبط
        
        Args:
            dto: داده‌های مورد نیاز برای بایگانی مقاله
            
        Returns:
            Article: مقاله بایگانی شده
            
        Raises:
            ArticleNotFoundError: اگر مقاله یافت نشود
            ArticlePermissionError: اگر کاربر مجوز بایگانی نداشته باشد
            InvalidArticleStatusError: اگر مقاله قابل بایگانی نباشد
        """
        # یافتن مقاله
        article = self.article_repository.get_by_id(dto.article_id)
        if not article:
            raise ArticleNotFoundError(dto.article_id)
        
        # بررسی مجوز بایگانی
        if not self._can_archive(article, dto.archiver):
            raise ArticlePermissionError(
                user_id=dto.archiver.id,
                article_id=dto.article_id
            )
        
        # بررسی وضعیت مقاله
        if article.status == ArticleStatus.ARCHIVED:
            return article  # اگر قبلا بایگانی شده، همان را برگردان
            
        if article.status not in [ArticleStatus.PUBLISHED, ArticleStatus.DRAFT]:
            raise InvalidArticleStatusError(
                current_status=article.status,
                expected_status=f"{ArticleStatus.PUBLISHED} یا {ArticleStatus.DRAFT}"
            )
        
        # بایگانی مقاله
        article.status = ArticleStatus.ARCHIVED
        
        # ذخیره تغییرات
        archived_article = self.article_repository.save(article)
        
        # حذف از موتور جستجو اگر منتشر شده بود
        if article.status == ArticleStatus.PUBLISHED:
            self.search_service.remove_article_from_index(article.id)
        
        return archived_article

    def _can_archive(self, article: Article, archiver: User) -> bool:
        """بررسی اینکه آیا کاربر مجوز بایگانی مقاله را دارد"""
        return (
            archiver.is_admin or 
            archiver.is_editor or 
            article.author.id == archiver.id
        )