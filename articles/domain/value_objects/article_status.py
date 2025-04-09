from enum import Enum

class ArticleStatus(str, Enum):
    """
    شیء مقدار برای وضعیت‌های مختلف مقاله
    """
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"

    @classmethod
    def get_choices(cls):
        """گزینه‌های قابل استفاده در فرم‌ها"""
        return [(item.value, item.name) for item in cls]