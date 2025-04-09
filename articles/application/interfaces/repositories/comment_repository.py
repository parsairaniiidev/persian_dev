from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.comment import Comment
from domain.value_objects.comment_status import CommentStatus

class CommentRepository(ABC):
    """اینترفیس ریپازیتوری برای مدیریت نظرات"""
    
    @abstractmethod
    def get_by_id(self, comment_id: str) -> Optional[Comment]:
        """یافتن نظر بر اساس شناسه"""
        pass
    
    @abstractmethod
    def save(self, comment: Comment) -> Comment:
        """ذخیره یا به‌روزرسانی نظر"""
        pass
    
    @abstractmethod
    def delete(self, comment_id: str) -> bool:
        """حذف نظر"""
        pass
    
    @abstractmethod
    def get_by_article(self, article_id: str, only_approved: bool = True) -> List[Comment]:
        """دریافت نظرات یک مقاله"""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: str) -> List[Comment]:
        """دریافت نظرات یک کاربر"""
        pass
    
    @abstractmethod
    def get_replies(self, parent_comment_id: str) -> List[Comment]:
        """دریافت پاسخ‌های یک نظر"""
        pass
    
    @abstractmethod
    def count_by_article(self, article_id: str, only_approved: bool = True) -> int:
        """شمردن نظرات یک مقاله"""
        pass
    
    @abstractmethod
    def get_pending_comments(self, page: int = 1, page_size: int = 10) -> List[Comment]:
        """دریافت نظرات در انتظار تایید"""
        pass
    
    @abstractmethod
    def change_status(self, comment_id: str, new_status: CommentStatus) -> bool:
        """تغییر وضعیت نظر"""
        pass
    
    @abstractmethod
    def get_recent_comments(self, limit: int = 5) -> List[Comment]:
        """دریافت آخرین نظرات"""
        pass