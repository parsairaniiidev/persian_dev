from abc import abstractmethod
from typing import Protocol, runtime_checkable
from domain.value_objects.content import Content

@runtime_checkable
class SpamDetectionService(Protocol):
    """رابطه تشخیص محتوای اسپم با پشتیبانی از الگوریتم‌های مختلف"""
    
    @abstractmethod
    def is_spam(self, content: Content) -> bool:
        """بررسی اسپم بودن محتوا"""
        pass

    @abstractmethod
    def analyze_patterns(self, content: Content) -> dict:
        """آنالیز الگوهای محتوا برای گزارش‌گیری"""
        pass

    @classmethod
    @abstractmethod
    def get_provider_info(cls) -> dict:
        """اطلاعات ارائه‌دهنده سرویس"""
        pass