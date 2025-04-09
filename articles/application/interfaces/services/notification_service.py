from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from domain.entities.notification import Notification
from core.domain.entities.user import User

@runtime_checkable
class NotificationService(Protocol):
    """رابطه سرویس اطلاع‌رسانی با قابلیت چندین کانال ارسال"""
    
    @abstractmethod
    def send(self, user: User, notification: Notification) -> bool:
        """ارسال اطلاع‌رسانی به کاربر"""
        pass

    @abstractmethod
    def broadcast(self, users: list[User], notification: Notification) -> dict[User, bool]:
        """ارسال گروهی اطلاع‌رسانی"""
        pass

    @property
    @abstractmethod
    def service_name(self) -> str:
        """نام سرویس برای لاگ‌گیری"""
        pass