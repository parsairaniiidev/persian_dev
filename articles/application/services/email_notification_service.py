# application/services/email_notification_service.py
from application.interfaces.services.notification_service import NotificationService
from infrastructure.external_services.email_provider import BaseEmailProvider

class EmailNotificationService(NotificationService):
    def __init__(self, email_provider: BaseEmailProvider):
        self._provider = email_provider

    def send(self, user, notification) -> bool:
        return self._provider.send_email(
            to=user.email,
            subject=notification.title,
            body=notification.content
        )

    @property
    def service_name(self) -> str:
        return "EmailNotificationService"