from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from core.domain.models.user import User
from domain.models.article import Article
from domain.models.comment import Comment
from domain.value_objects.comment_status import CommentStatus
from domain.exceptions.comment_errors import (
    CommentValidationError,
    CommentSpamDetectedError,
    CommentReplyDepthExceededError
)
from application.interfaces.repositories.article_repository import ArticleRepository
from application.interfaces.repositories.comment_repository import CommentRepository
from application.interfaces.services.spam_detection_service import SpamDetectionService
from application.interfaces.services.notification_service import NotificationService

@dataclass
class AddCommentDTO:
    """شیء انتقال داده برای افزودن کامنت"""
    article_id: str
    content: str
    author: User
    parent_comment_id: str | None = None

class AddCommentUseCase:
    """یوزکیس افزودن کامنت جدید"""
    
    def __init__(
        self,
        article_repository: ArticleRepository,
        comment_repository: CommentRepository,
        spam_detection_service: SpamDetectionService,
        notification_service: NotificationService,
        max_reply_depth: int = 3
    ):
        self.article_repository = article_repository
        self.comment_repository = comment_repository
        self.spam_detection_service = spam_detection_service
        self.notification_service = notification_service
        self.max_reply_depth = max_reply_depth

    def execute(self, dto: AddCommentDTO) -> Comment:
        """
        افزودن کامنت جدید به مقاله با اعتبارسنجی
        
        Args:
            dto: داده‌های مورد نیاز برای افزودن کامنت
            
        Returns:
            Comment: کامنت ایجاد شده
            
        Raises:
            CommentValidationError: اگر داده‌ها نامعتبر باشند
            CommentSpamDetectedError: اگر کامنت اسپم تشخیص داده شود
            CommentReplyDepthExceededError: اگر عمق پاسخ‌دهی بیش از حد مجاز باشد
        """
        # اعتبارسنجی داده‌های ورودی
        self._validate_input(dto)
        
        # بررسی اسپم بودن کامنت
        if self.spam_detection_service.is_spam(dto.content):
            raise CommentSpamDetectedError()
        
        # یافتن مقاله
        article = self.article_repository.get_by_id(dto.article_id)
        if not article:
            raise CommentValidationError(
                field_name="article_id",
                error_message="مقاله مورد نظر یافت نشد"
            )
        
        # بررسی عمق پاسخ‌دهی برای کامنت‌های پاسخ
        if dto.parent_comment_id:
            parent_comment = self.comment_repository.get_by_id(dto.parent_comment_id)
            if not parent_comment:
                raise CommentValidationError(
                    field_name="parent_comment_id",
                    error_message="کامنت والد یافت نشد"
                )
            
            reply_depth = self._calculate_reply_depth(parent_comment)
            if reply_depth >= self.max_reply_depth:
                raise CommentReplyDepthExceededError(self.max_reply_depth)
        
        # ایجاد کامنت جدید
        new_comment = Comment(
            content=dto.content,
            author=dto.author,
            article_id=dto.article_id,
            parent_id=dto.parent_comment_id
        )
        
        # ذخیره کامنت
        saved_comment = self.comment_repository.save(new_comment)
        
        # ارسال نوتیفیکیشن
        self.notification_service.send_new_comment_notification(
            comment=saved_comment,
            article=article
        )
        
        return saved_comment

    def _validate_input(self, dto: AddCommentDTO) -> None:
        """اعتبارسنجی داده‌های ورودی"""
        if not dto.content or len(dto.content.strip()) < 10:
            raise CommentValidationError(
                field_name="content",
                error_message="متن کامنت باید حداقل ۱۰ کاراکتر داشته باشد"
            )
            
        if len(dto.content) > 1000:
            raise CommentValidationError(
                field_name="content",
                error_message="متن کامنت نمی‌تواند بیش از ۱۰۰۰ کاراکتر باشد"
            )

    def _calculate_reply_depth(self, comment: Comment) -> int:
        """محاسبه عمق پاسخ‌دهی برای یک کامنت"""
        depth = 0
        current = comment
        
        while current.parent_id:
            parent = self.comment_repository.get_by_id(current.parent_id)
            if not parent:
                break
            depth += 1
            current = parent
            
        return depth