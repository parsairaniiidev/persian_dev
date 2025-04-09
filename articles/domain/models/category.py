from dataclasses import dataclass
from uuid import uuid4
from domain.value_objects.slug import Slug

@dataclass
class Category:
    """
    موجودیت دسته‌بندی مقالات
    شامل سلسله مراتب و اطلاعات مربوط به هر دسته
    """
    id: str
    name: str
    slug: Slug
    description: str
    parent_id: str | None
    is_active: bool

    def __init__(
        self,
        name: str,
        description: str = "",
        parent_id: str = None,
        is_active: bool = True
    ):
        self.id = str(uuid4())
        self.name = name
        self.slug = Slug.generate_from_title(name)
        self.description = description
        self.parent_id = parent_id
        self.is_active = is_active

    def deactivate(self) -> None:
        """غیرفعال کردن دسته‌بندی"""
        self.is_active = False

    def update_info(self, name: str, description: str) -> None:
        """به‌روزرسانی اطلاعات دسته‌بندی"""
        self.name = name
        self.slug = Slug.generate_from_title(name)
        self.description = description