# core/application/use_cases/authentication/two_factor.py
import random
from datetime import datetime, timedelta
from core.domain.exceptions import TwoFactorCodeExpiredError, InvalidTwoFactorCodeError

class TwoFactorUseCase:
    """
    مدیریت احراز هویت دو مرحله‌ای
    """
    CODE_VALID_MINUTES = 5

    def __init__(self, sms_service, cache):
        self.sms_service = sms_service
        self.cache = cache

    def generate_code(self, user_id: int) -> str:
        """تولید کد تصادفی ۶ رقمی"""
        code = str(random.randint(100000, 999999))
        self.cache.set(
            f"2fa_{user_id}",
            {'code': code, 'attempts': 0},
            timeout=60 * self.CODE_VALID_MINUTES
        )
        return code

    def verify_code(self, user_id: int, entered_code: str) -> bool:
        """اعتبارسنجی کد وارد شده"""
        cached = self.cache.get(f"2fa_{user_id}")
        
        if not cached:
            raise TwoFactorCodeExpiredError()
        
        if cached['attempts'] >= 3:
            self.cache.delete(f"2fa_{user_id}")
            raise TwoFactorCodeExpiredError("تعداد تلاش‌ها بیش از حد مجاز")
        
        if cached['code'] != entered_code:
            cached['attempts'] += 1
            self.cache.set(f"2fa_{user_id}", cached)
            raise InvalidTwoFactorCodeError()
        
        self.cache.delete(f"2fa_{user_id}")
        return True