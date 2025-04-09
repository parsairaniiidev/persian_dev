# core/application/use_cases/authentication/login_use_case.py
from datetime import datetime
from django.contrib.auth import authenticate
from core.domain.exceptions import (
    InvalidCredentialsError,
    AccountLockedError,
    TwoFactorRequiredError
)
from core.infrastructure.security.jwt_provider import JWTProvider
from core.domain.events import UserLoggedInEvent
from core.infrastructure.events import DjangoEventPublisher

class LoginUseCase:
    def __init__(
        self,
        user_repository,
        auth_service: JWTProvider,
        event_publisher: DjangoEventPublisher,
        max_attempts: int = 5
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.event_publisher = event_publisher
        self.max_attempts = max_attempts

    def execute(self, command):
        user = self.user_repository.find_by_email(command.email)
        
        if user.failed_login_attempts >= self.max_attempts:
            raise AccountLockedError("حساب کاربری به دلیل ورودهای ناموفق قفل شده است")

        if not self.auth_service.verify_password(command.password, user.password_hash):
            user.failed_login_attempts += 1
            user.save(update_fields=['failed_login_attempts'])
            raise InvalidCredentialsError()

        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.now()
        user.save(update_fields=['failed_login_attempts', 'last_login'])

        # Publish domain event
        self.event_publisher.publish(UserLoggedInEvent(
            user_id=user.id,
            login_time=datetime.now(),
            ip_address=command.ip_address
        ))

        if user.two_factor_enabled:
            raise TwoFactorRequiredError()

        return {
            'access_token': self.auth_service.generate_access_token(user),
            'refresh_token': self.auth_service.generate_refresh_token(user)
        }