from dataclasses import dataclass
from uuid import uuid4
from domain.value_objects.slug import Slug

@dataclass
class Tag:
    """
    موجودیت تگ برای مقالات
    شامل اطلاعات پایه و مدیریت تگ‌ها
    """
    id: str
    name: str
    slug: Slug
    description: str
    usage_count: int

    def __init__(self, name: str, description: str = ""):
        self.id = str(uuid4())
        self.name = name
        self.slug = Slug.generate_from_title(name)
        self.description = description
        self.usage_count = 0

    def increment_usage(self) -> None:
        """افزایش تعداد استفاده از تگ"""
        self.usage_count += 1

    def update_info(self, name: str, description: str) -> None:
        """به‌روزرسانی اطلاعات تگ"""
        self.name = name
        self.slug = Slug.generate_from_title(name)
        self.description = description