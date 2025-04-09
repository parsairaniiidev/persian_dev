from enum import Enum

class CommentStatus(str, Enum):
    """
    شیء مقدار برای وضعیت‌های مختلف کامنت
    """
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SPAM = "spam"

    @classmethod
    def get_choices(cls):
        """گزینه‌های قابل استفاده در فرم‌ها"""
        return [(item.value, item.name) for item in cls]