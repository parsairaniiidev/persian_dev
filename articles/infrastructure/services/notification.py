# infrastructure/services/notification.py
import logging
from domain.entities.notification import Notification
from core.domain.entities.user import User
from infrastructure.external_services.email_provider import EmailProvider

logger = logging.getLogger(__name__)

class EmailNotificationService:
    """Email notification service implementation"""
    
    def __init__(self, email_provider: EmailProvider):
        self.email_provider = email_provider
        logger.info("Initialized EmailNotificationService")

    def send(self, user: User, notification: Notification) -> bool:
        """Send email notification to user"""
        try:
            logger.debug(f"Sending notification to {user.email}")
            return self.email_provider.send(
                to=user.email,
                subject=notification.title,
                body=notification.content,
                metadata=notification.metadata
            )
        except Exception as e:
            logger.error(f"Notification failed: {str(e)}")
            return False