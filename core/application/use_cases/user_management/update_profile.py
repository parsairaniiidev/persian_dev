# core/application/use_cases/user_management/update_profile.py
from datetime import datetime
from core.domain.exceptions import UserNotFoundError, ValidationError
from core.domain.value_objects import Email
from core.domain.events import ProfileUpdatedEvent
from core.infrastructure.events import DjangoEventPublisher

class UpdateProfileUseCase:
    """
    سرویس به‌روزرسانی پروفایل کاربر با اعتبارسنجی پیشرفته
    """
    def __init__(self, user_repository, event_publisher: DjangoEventPublisher):
        self.user_repository = user_repository
        self.event_publisher = event_publisher

    def execute(self, user_id: int, update_data: dict):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        
        # اعتبارسنجی و به‌روزرسانی فیلدها
        if 'email' in update_data:
            new_email = Email(update_data['email'])
            self._validate_email(new_email)
            user.email = new_email.address
        
        if 'username' in update_data:
            self._validate_username(update_data['username'])
            user.username = update_data['username']
        
        self.user_repository.update(user)
        
        # انتشار رویداد دامنه
        self.event_publisher.publish(ProfileUpdatedEvent(
            user_id=user.id,
            updated_fields=list(update_data.keys()),
            updated_at=datetime.now()
        ))

    def _validate_email(self, email: Email):
        """اعتبارسنجی ایمیل"""
        if self.user_repository.exists_by_email(email.address):
            raise ValidationError("این ایمیل قبلاً ثبت شده است")

    def _validate_username(self, username: str):
        """اعتبارسنجی نام کاربری"""
        if len(username) < 4:
            raise ValidationError("نام کاربری باید حداقل ۴ کاراکتر باشد")
        if not username.isalnum():
            raise ValidationError("نام کاربری فقط می‌تواند شامل حروف و اعداد باشد")