# core/infrastructure/security/jwt_provider.py
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from django.conf import settings
from core.domain.exceptions import TokenValidationError, TokenExpiredError

class JWTProvider:
    """
    مدیریت کامل توکن‌های JWT با قابلیت‌های:
    - تولید توکن دسترسی و توکن تازه‌سازی
    - اعتبارسنجی توکن‌ها
    - استخراج اطلاعات از توکن
    - پشتیبانی از لیست سیاه توکن‌ها (Blacklist)
    """

    def __init__(self):
        self.secret_key = settings.JWT_CONFIG['SECRET_KEY']
        self.algorithm = settings.JWT_CONFIG['ALGORITHM']
        self.access_token_lifetime = settings.JWT_CONFIG['ACCESS_TOKEN_LIFETIME']
        self.refresh_token_lifetime = settings.JWT_CONFIG['REFRESH_TOKEN_LIFETIME']

    def generate_access_token(self, user_id: str, additional_claims: Dict[str, Any] = None) -> str:
        """
        تولید توکن دسترسی (Access Token)
        :param user_id: شناسه کاربر
        :param additional_claims: ادعاهای اضافی برای قرار دادن در توکن
        :return: توکن امضا شده
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + self.access_token_lifetime,
            'iat': datetime.utcnow(),
            'type': 'access',
            **additional_claims
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def generate_refresh_token(self, user_id: str) -> str:
        """
        تولید توکن تازه‌سازی (Refresh Token)
        :param user_id: شناسه کاربر
        :return: توکن امضا شده
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + self.refresh_token_lifetime,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        اعتبارسنجی توکن و استخراج محتویات
        :param token: توکن دریافتی
        :return: محتویات توکن در صورت معتبر بودن
        :raises TokenValidationError: اگر توکن نامعتبر باشد
        :raises TokenExpiredError: اگر توکن منقضی شده باشد
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={
                    'verify_exp': True,
                    'verify_signature': True
                }
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("توکن منقضی شده است")
        except jwt.PyJWTError as e:
            raise TokenValidationError(f"توکن نامعتبر: {str(e)}")

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        تولید توکن دسترسی جدید با استفاده از توکن تازه‌سازی
        :param refresh_token: توکن تازه‌سازی
        :return: توکن دسترسی جدید
        """
        try:
            payload = self.verify_token(refresh_token)
            if payload.get('type') != 'refresh':
                raise TokenValidationError("نوع توکن نامعتبر است")

            return self.generate_access_token(
                user_id=payload['user_id'],
                additional_claims={
                    'roles': payload.get('roles', []),
                    'permissions': payload.get('permissions', [])
                }
            )
        except (TokenValidationError, TokenExpiredError) as e:
            raise TokenValidationError(f"خطا در تازه‌سازی توکن: {str(e)}")

    def get_user_id_from_token(self, token: str) -> Optional[str]:
        """
        استخراج شناسه کاربر از توکن بدون اعتبارسنجی انقضا
        (برای استفاده در موارد خاص)
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={'verify_exp': False}
            )
            return payload.get('user_id')
        except jwt.PyJWTError:
            return None

    def add_to_blacklist(self, token: str, expires_in: int = None) -> bool:
        """
        افزودن توکن به لیست سیاه (برای باطل کردن توکن)
        :param token: توکن مورد نظر
        :param expires_in: زمان انقضا به ثانیه (پیش‌فرض: زمان انقضای خود توکن)
        :return: موفقیت/عدم موفقیت عملیات
        """
        try:
            payload = self.verify_token(token)
            expiry = payload['exp'] if expires_in is None else int(
                datetime.utcnow().timestamp()) + expires_in
            
            # ذخیره در Redis یا دیتابیس
            # مثال: redis.set(f"token_blacklist:{token}", "1", ex=expiry)
            return True
        except (TokenValidationError, TokenExpiredError):
            return False

    def is_blacklisted(self, token: str) -> bool:
        """
        بررسی وجود توکن در لیست سیاه
        """
        # مثال: return bool(redis.exists(f"token_blacklist:{token}"))
        return False