# core/application/services/auth_service.py
from datetime import datetime, timedelta

from django.conf import settings
from core.domain.exceptions import AuthenticationError, InvalidTwoFactorCodeError, TwoFactorCodeExpiredError
from core.domain.models.user import User
from core.infrastructure.security.jwt_provider import JWTProvider
from core.infrastructure.security.password_hasher import AdvancedPasswordHasher

# مثال استفاده در سرویس احراز هویت
from core.application.interfaces.services.sms_service import ISmsService
from core.infrastructure.services.sms.kavenegar_sms_service import KavenegarSMSService


class AuthService:
    """
    سرویس احراز هویت پیشرفته با قابلیت‌های:
    - ورود
    - بازنشانی رمز
    - مدیریت توکن‌ها
    """
    def __init__(self, sms_service: ISmsService = None):
        self.sms_service = sms_service or KavenegarSmsService()
    
    def send_login_otp(self, phone_number: str):
        code = self._generate_otp_code()
        if self.sms_service.send_otp(phone_number, code):
            # ذخیره کد در کش با کلید phone_number
            return True
        return False

    def __init__(self, jwt_provider: JWTProvider, password_hasher: AdvancedPasswordHasher):
        self.jwt_provider = jwt_provider
        self.password_hasher = password_hasher
    
    def authenticate(self, email: str, password: str, user) -> dict:
        """احراز هویت کاربر"""
        if not user or not self.password_hasher.verify_password(password, user.password_hash):
            raise AuthenticationError("اطلاعات ورود نامعتبر است")
        
        return {
            'access_token': self.jwt_provider.generate_token(user),
            'refresh_token': self.jwt_provider.generate_refresh_token(user)
        }
    
    def refresh_token(self, refresh_token: str) -> dict:
        """تازه‌سازی توکن دسترسی"""
        payload = self.jwt_provider.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            raise AuthenticationError("توکن نامعتبر است")
        
        return {
            'access_token': self.jwt_provider.generate_token_by_payload(payload),
            'refresh_token': refresh_token
        }
    
class TwoFactorService:
    def verify_code(self, user_id, code_type, code):
        """Verifies a 2FA code with proper error handling"""
        user = User.objects.get(pk=user_id)
        code_record = self._get_code_record(user, code_type)
        
        # Check expiration first
        if datetime.now() > code_record.expires_at:
            raise TwoFactorCodeExpiredError(
                user_id=user_id,
                code_type=code_type,
                expires_at=code_record.expires_at
            )
            
        # Then check validity
        if not self._validate_code(code_record, code):
            attempts = user.increment_2fa_attempts()
            raise InvalidTwoFactorCodeError.with_retry_info(
                user_id=user_id,
                code_type=code_type,
                max_attempts=settings.MAX_2FA_ATTEMPTS,
                attempts_made=attempts
            )
            
        # Reset attempts on success
        user.reset_2fa_attempts()
        return True