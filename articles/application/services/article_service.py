# application/services/article_service.py
from dependency_injector import containers, providers

from articles.application.interfaces.services.notification_service import NotificationService
from articles.application.interfaces.services.spam_detection_service import SpamDetectionService
from articles.application.services.ai_spam_detection_service import AISpamDetectionService
from articles.application.services.email_notification_service import EmailNotificationService
from articles.domain.models.notification import Notification

class ArticleService:
    def __init__(
        self,
        notification_service: NotificationService,
        spam_detection_service: SpamDetectionService
    ):
        self._notifier = notification_service
        self._spam_detector = spam_detection_service

    def publish_article(self, article, user):
        if self._spam_detector.is_spam(article.content):
            raise ValueError("محتوای مقاله به عنوان اسپم تشخیص داده شد")
        
        article.publish()
        self._notifier.send(user, Notification(
            title="مقاله شما منتشر شد",
            content=f"مقاله {article.title} با موفقیت منتشر شد"
        ))

class ServiceContainer(containers.DeclarativeContainer):
    notification = providers.Singleton(EmailNotificationService)
    spam_detection = providers.Singleton(AISpamDetectionService)
    article_service = providers.Factory(
        ArticleService,
        notification_service=notification,
        spam_detection_service=spam_detection
    )