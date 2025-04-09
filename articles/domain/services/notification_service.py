# domain/services/notification_service.py
from abc import ABC, abstractmethod
from domain.entities.notification import Notification
from core.domain.entities.user import User

class NotificationService(ABC):
    @abstractmethod
    def send(self, user: User, notification: Notification) -> bool:
        pass