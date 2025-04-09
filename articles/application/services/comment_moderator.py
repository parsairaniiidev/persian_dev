from typing import List, Optional
from domain.models.comment import Comment
from domain.value_objects.comment_status import CommentStatus
from application.interfaces.repositories.comment_repository import CommentRepository
from application.interfaces.services.notification_service import NotificationService
from application.interfaces.services.spam_detection_service import SpamDetectionService

class CommentModerator:
    """سرویس مدیریت و نظارت بر نظرات"""
    
    def __init__(
        self,
        comment_repository: CommentRepository,
        spam_detection_service: SpamDetectionService,
        notification_service: NotificationService,
        auto_approve_threshold: int = 3
    ):
        self.comment_repo = comment_repository
        self.spam_detector = spam_detection_service
        self.notifier = notification_service
        self.auto_approve_threshold = auto_approve_threshold

    def moderate_new_comment(self, comment: Comment) -> Comment:
        """
        بررسی و مدیریت خودکار نظر جدید
        Args:
            comment: نظر جدید
        Returns:
            Comment: نظر پس از مدیریت
        """
        # تشخیص اسپم
        if self.spam_detector.is_spam(comment.content):
            comment.status = CommentStatus.SPAM
        else:
            # تایید خودکار برای کاربران معتبر
            if self._should_auto_approve(comment.author.id):
                comment.approve()
                self.notifier.send_comment_approved_notification(comment)
            else:
                comment.status = CommentStatus.PENDING
        
        return self.comment_repo.save(comment)

    def batch_approve_comments(self, comment_ids: List[str]) -> dict:
        """
        تایید گروهی نظرات
        Args:
            comment_ids: لیست شناسه نظرات
        Returns:
            dict: آمار عملیات
        """
        results = {
            'total': len(comment_ids),
            'approved': 0,
            'failed': 0
        }
        
        for comment_id in comment_ids:
            try:
                comment = self.comment_repo.get_by_id(comment_id)
                if comment and comment.status == CommentStatus.PENDING:
                    comment.approve()
                    self.comment_repo.save(comment)
                    self.notifier.send_comment_approved_notification(comment)
                    results['approved'] += 1
            except Exception:
                results['failed'] += 1
        
        return results

    def _should_auto_approve(self, user_id: str) -> bool:
        """
        بررسی آیا نظر کاربر باید به صورت خودکار تایید شود
        Args:
            user_id: شناسه کاربر
        Returns:
            bool: نتیجه بررسی
        """
        user_comments = self.comment_repo.get_by_user(user_id)
        approved_comments = [c for c in user_comments if c.status == CommentStatus.APPROVED]
        return len(approved_comments) >= self.auto_approve_threshold

    def detect_spam_comments(self, batch_size: int = 100) -> dict:
        """
        بررسی نظرات در انتظار برای تشخیص اسپم
        Args:
            batch_size: تعداد نظرات در هر بسته
        Returns:
            dict: آمار عملیات
        """
        stats = {
            'total_checked': 0,
            'spam_detected': 0,
            'approved': 0
        }
        
        page = 1
        while True:
            comments = self.comment_repo.get_pending_comments(page, batch_size)
            if not comments:
                break
            
            for comment in comments:
                try:
                    if self.spam_detector.is_spam(comment.content):
                        comment.status = CommentStatus.SPAM
                        stats['spam_detected'] += 1
                    elif self._should_auto_approve(comment.author.id):
                        comment.approve()
                        stats['approved'] += 1
                    
                    self.comment_repo.save(comment)
                    stats['total_checked'] += 1
                except Exception:
                    continue
            
            page += 1
        
        return stats