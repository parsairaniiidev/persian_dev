from dataclasses import dataclass
from core.domain.models.user import User
from domain.models.comment import Comment
from domain.value_objects.comment_status import CommentStatus
from domain.exceptions.comment_errors import (
    CommentNotFoundError,
    CommentPermissionError,
    CommentAlreadyApprovedError,
    InvalidCommentStatusError
)
from application.interfaces.repositories.comment_repository import CommentRepository
from application.interfaces.services.notification_service import NotificationService

@dataclass
class ModerateCommentDTO:
    """شیء انتقال داده برای مدیریت کامنت"""
    comment_id: str
    action: str  # 'approve' یا 'reject' یا 'spam'
    moderator: User

class ModerateCommentUseCase:
    """یوزکیس مدیریت کامنت (تایید/رد/علامت‌گذاری به عنوان اسپم)"""
    
    def __init__(
        self,
        comment_repository: CommentRepository,
        notification_service: NotificationService
    ):
        self.comment_repository = comment_repository
        self.notification_service = notification_service

    def execute(self, dto: ModerateCommentDTO) -> Comment:
        """
        مدیریت کامنت (تایید/رد/اسپم)
        
        Args:
            dto: داده‌های مورد نیاز برای مدیریت کامنت
            
        Returns:
            Comment: کامنت مدیریت شده
            
        Raises:
            CommentNotFoundError: اگر کامنت یافت نشود
            CommentPermissionError: اگر کاربر مجوز مدیریت نداشته باشد
            CommentAlreadyApprovedError: اگر کامنت قبلا تایید شده باشد
            InvalidCommentStatusError: اگر عمل نامعتبر باشد
        """
        # یافتن کامنت
        comment = self.comment_repository.get_by_id(dto.comment_id)
        if not comment:
            raise CommentNotFoundError(dto.comment_id)
        
        # بررسی مجوز مدیریت
        if not dto.moderator.is_admin and not dto.moderator.is_moderator:
            raise CommentPermissionError(
                user_id=dto.moderator.id,
                comment_id=dto.comment_id
            )
        
        # اعمال عمل مدیریت
        if dto.action == 'approve':
            if comment.status == CommentStatus.APPROVED:
                raise CommentAlreadyApprovedError(dto.comment_id)
            comment.approve()
        
        elif dto.action == 'reject':
            if comment.status == CommentStatus.REJECTED:
                return comment  # اگر قبلا رد شده، همان را برگردان
            comment.reject()
        
        elif dto.action == 'spam':
            comment.status = CommentStatus.SPAM
        
        else:
            raise InvalidCommentStatusError(
                current_status=comment.status,
                expected_status="approve/reject/spam"
            )
        
        # ذخیره تغییرات
        moderated_comment = self.comment_repository.save(comment)
        
        # ارسال نوتیفیکیشن به نویسنده کامنت (در صورت تایید یا رد)
        if dto.action in ['approve', 'reject']:
            self.notification_service.send_comment_moderation_notification(
                comment=moderated_comment,
                action=dto.action
            )
        
        return moderated_comment