from dataclasses import dataclass
from articles.domain.value_objects.article_status import ArticleStatus
from core.domain.models.user import User
from domain.models.article import Article
from domain.exceptions.article_errors import (
    ArticleNotFoundError,
    ArticlePermissionError,
    ArticleAlreadyPublishedError,
    ArticleValidationError
)
from application.interfaces.repositories.article_repository import ArticleRepository
from application.interfaces.services.search_service import SearchService
from application.interfaces.services.notification_service import NotificationService

@dataclass
class PublishArticleDTO:
    """شیء انتقال داده برای انتشار مقاله"""
    article_id: str
    publisher: User  # کاربری که در حال انتشار مقاله است

class PublishArticleUseCase:
    """یوزکیس انتشار مقاله"""
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        search_service: SearchService,
        notification_service: NotificationService
    ):
        self.article_repository = article_repository
        self.search_service = search_service
        self.notification_service = notification_service

    def execute(self, dto: PublishArticleDTO) -> Article:
        """
        انتشار مقاله با اعتبارسنجی و انجام عملیات مرتبط
        
        Args:
            dto: داده‌های مورد نیاز برای انتشار مقاله
            
        Returns:
            Article: مقاله منتشر شده
            
        Raises:
            ArticleNotFoundError: اگر مقاله یافت نشود
            ArticlePermissionError: اگر کاربر مجوز انتشار نداشته باشد
            ArticleAlreadyPublishedError: اگر مقاله قبلا منتشر شده باشد
            ArticleValidationError: اگر مقاله قابل انتشار نباشد
        """
        # یافتن مقاله
        article = self.article_repository.get_by_id(dto.article_id)
        if not article:
            raise ArticleNotFoundError(dto.article_id)
        
        # بررسی مجوز انتشار
        if not self._can_publish(article, dto.publisher):
            raise ArticlePermissionError(
                user_id=dto.publisher.id,
                article_id=dto.article_id
            )
        
        # بررسی وضعیت مقاله
        if article.status == ArticleStatus.PUBLISHED:
            raise ArticleAlreadyPublishedError(dto.article_id)
        
        # اعتبارسنجی مقاله برای انتشار
        self._validate_for_publishing(article)
        
        # انتشار مقاله
        article.publish()
        
        # ذخیره تغییرات
        published_article = self.article_repository.save(article)
        
        # اندیس کردن مقاله در موتور جستجو
        self.search_service.index_article(published_article)
        
        # ارسال نوتیفیکیشن
        self.notification_service.send_article_published_notification(
            article=published_article,
            publisher=dto.publisher
        )
        
        return published_article

    def _can_publish(self, article: Article, publisher: User) -> bool:
        """بررسی اینکه آیا کاربر مجوز انتشار مقاله را دارد"""
        return (
            publisher.is_admin or 
            publisher.is_editor or 
            (article.author.id == publisher.id and publisher.can_publish)
        )

    def _validate_for_publishing(self, article: Article) -> None:
        """اعتبارسنجی مقاله برای انتشار"""
        if not article.content or len(article.content.strip()) < 300:
            raise ArticleValidationError(
                field_name="content",
                error_message="برای انتشار، محتوای مقاله باید حداقل ۳۰۰ کاراکتر داشته باشد"
            )
            
        if not article.tags:
            raise ArticleValidationError(
                field_name="tags",
                error_message="برای انتشار، مقاله باید حداقل یک تگ داشته باشد"
            )