from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass
from core.domain.models.user import User
from domain.value_objects.comment_status import CommentStatus

@dataclass
class Comment:
    """
    موجودیت کامنت با قوانین مربوط به نظرات
    شامل وضعیت‌های مختلف و اعتبارسنجی‌ها
    """
    id: str
    content: str
    author: User
    article_id: str
    status: CommentStatus
    created_at: datetime
    updated_at: datetime
    parent_id: str | None

    def __init__(
        self,
        content: str,
        author: User,
        article_id: str,
        parent_id: str = None
    ):
        self.id = str(uuid4())
        self.content = content
        self.author = author
        self.article_id = article_id
        self.status = CommentStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.parent_id = parent_id

    def approve(self) -> None:
        """تایید کامنت توسط مدیر"""
        self.status = CommentStatus.APPROVED
        self.updated_at = datetime.now()

    def reject(self) -> None:
        """رد کامنت توسط مدیر"""
        self.status = CommentStatus.REJECTED
        self.updated_at = datetime.now()

    def update_content(self, new_content: str) -> None:
        """به‌روزرسانی محتوای کامنت"""
        if len(new_content) < 10:
            raise ValueError("متن کامنت باید حداقل ۱۰ کاراکتر داشته باشد")
        self.content = new_content
        self.updated_at = datetime.now()