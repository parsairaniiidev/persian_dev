from kavenegar import KavenegarAPI
from django.conf import settings
from core.application.interfaces.services.sms_service import ISmsService

class KavenegarSMSService(ISmsService):
    """
    پیاده‌سازی سرویس پیامک با کاوه‌نگار (سرویس ایرانی)
    """
    def __init__(self):
        self.api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    
    def send_sms(self, phone_number: str, message: str) -> bool:
        try:
            params = {
                'sender': settings.KAVENEGAR_SENDER_NUMBER,
                'receptor': phone_number,
                'message': message
            }
            response = self.api.sms_send(params)
            return response[0]['status'] == 5  # کد وضعیت موفقیت‌آمیز
        except Exception as e:
            # لاگ خطا
            return False
    
    def send_otp(self, phone_number: str, code: str) -> bool:
        template = settings.KAVENEGAR_OTP_TEMPLATE
        try:
            params = {
                'receptor': phone_number,
                'template': template,
                'token': code
            }
            response = self.api.verify_lookup(params)
            return response[0]['status'] == 5
        except Exception:
            return False