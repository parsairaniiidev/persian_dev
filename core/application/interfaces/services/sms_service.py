# core/application/interfaces/services/sms_service.py
from abc import ABC, abstractmethod

class ISmsService(ABC):
    """
    اینترفیس سرویس ارسال پیامک
    """
    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> bool:
        pass
    
    @abstractmethod
    def send_otp(self, phone_number: str, code: str) -> bool:
        pass