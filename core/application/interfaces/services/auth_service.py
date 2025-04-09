from abc import ABC, abstractmethod
from typing import Optional
from core.domain.models.user import User
from core.domain.exceptions import (
    InvalidCredentialsError,
    UserNotFoundError,
    AccountLockedError
)
from core.application.interfaces.repositories.user_repository import IUserRepository
from core.application.interfaces.services.auth_service import IPasswordHasher, IJWTProvider

class AuthenticationService:
    """
    سرویس احراز هویت کاربران
    مسئولیت‌ها:
    - ثبت نام کاربر جدید
    - ورود کاربر
    - بازنشانی رمز عبور
    - احراز توکن JWT
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        jwt_provider: IJWTProvider,
        max_login_attempts: int = 5
    ):
        self._user_repo = user_repository
        self._hasher = password_hasher
        self._jwt = jwt_provider
        self._max_attempts = max_login_attempts

    def register(self, email: str, password: str, **kwargs) -> User:
        """
        ثبت نام کاربر جدید
        :param email: آدرس ایمیل کاربر
        :param password: رمز عبور
        :param kwargs: اطلاعات اضافی کاربر
        :return: کاربر ایجاد شده
        """
        if self._user_repo.exists(email):
            raise ValueError("کاربر با این ایمیل قبلا ثبت نام کرده است")

        hashed_password = self._hasher.hash_password(password)
        user = User(email=email, password_hash=hashed_password, **kwargs)
        
        return self._user_repo.add(user)

    def login(self, email: str, password: str) -> str:
        """
        ورود کاربر و دریافت توکن
        :param email: آدرس ایمیل
        :param password: رمز عبور
        :return: توکن JWT
        :raises: InvalidCredentialsError اگر احراز هویت ناموفق باشد
        """
        user = self._user_repo.get_by_email(email)
        if not user:
            raise UserNotFoundError("کاربر یافت نشد")

        if user.failed_login_attempts >= self._max_attempts:
            raise AccountLockedError("حساب کاربری به دلیل ورودهای ناموفق قفل شده است")

        if not self._hasher.verify_password(password, user.password_hash):
            user.failed_login_attempts += 1
            self._user_repo.update(user)
            raise InvalidCredentialsError("ایمیل یا رمز عبور اشتباه است")

        # Reset attempts on successful login
        user.failed_login_attempts = 0
        self._user_repo.update(user)

        return self._jwt.generate_token(user.id)

    def verify_token(self, token: str) -> Optional[User]:
        """
        اعتبارسنجی توکن JWT
        :param token: توکن دریافتی
        :return: کاربر مربوطه اگر توکن معتبر باشد
        """
        user_id = self._jwt.validate_token(token)
        if user_id:
            return self._user_repo.get(user_id)
        return None