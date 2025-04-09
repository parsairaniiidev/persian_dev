# core/application/services/user_service.py
from core.domain.exceptions import UserNotFoundError
from core.domain.events import (
    PasswordChangedEvent,
    ProfileUpdatedEvent
)

class UserService:
    """
    سرویس مدیریت کاربران با قابلیت‌های:
    - به‌روزرسانی پروفایل
    - تغییر رمز عبور
    - مدیریت نقش‌ها
    """
    def __init__(self, user_repository, event_publisher):
        self.user_repository = user_repository
        self.event_publisher = event_publisher
    
    def update_profile(self, user_id: int, update_data: dict) -> None:
        """به‌روزرسانی اطلاعات کاربر"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        
        # اعمال تغییرات
        if 'email' in update_data:
            user.email = update_data['email']
        
        self.user_repository.update(user)
        
        # انتشار رویداد
        self.event_publisher.publish(ProfileUpdatedEvent(
            user_id=user.id,
            changes=update_data
        ))
    
    def change_password(self, user_id: int, new_password: str) -> None:
        """تغییر رمز عبور کاربر"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        
        user.password_hash = self.password_hasher.hash_password(new_password)
        self.user_repository.update(user)
        
        self.event_publisher.publish(PasswordChangedEvent(
            user_id=user.id
        ))