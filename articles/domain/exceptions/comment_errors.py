class CommentError(Exception):
    """خطای پایه برای تمام خطاهای مربوط به نظرات"""
    pass


class CommentNotFoundError(CommentError):
    """کامنت مورد نظر یافت نشد"""
    
    def __init__(self, comment_id=None):
        self.comment_id = comment_id
        message = "نظر مورد نظر یافت نشد"
        if comment_id:
            message = f"نظر با شناسه {comment_id} یافت نشد"
        super().__init__(message)


class CommentAlreadyApprovedError(CommentError):
    """کامنت قبلا تایید شده است"""
    
    def __init__(self, comment_id=None):
        self.comment_id = comment_id
        message = "نظر قبلا تایید شده است"
        if comment_id:
            message = f"نظر با شناسه {comment_id} قبلا تایید شده است"
        super().__init__(message)


class InvalidCommentStatusError(CommentError):
    """وضعیت کامنت نامعتبر است"""
    
    def __init__(self, current_status, expected_status=None):
        self.current_status = current_status
        self.expected_status = expected_status
        message = f"وضعیت فعلی نظر ({current_status}) نامعتبر است"
        if expected_status:
            message += f"، وضعیت مورد انتظار: {expected_status}"
        super().__init__(message)


class CommentPermissionError(CommentError):
    """دسترسی به کامنت مجاز نیست"""
    
    def __init__(self, user_id=None, comment_id=None):
        self.user_id = user_id
        self.comment_id = comment_id
        message = "دسترسی به این نظر مجاز نیست"
        if user_id and comment_id:
            message = f"کاربر با شناسه {user_id} اجازه دسترسی به نظر {comment_id} را ندارد"
        super().__init__(message)


class CommentValidationError(CommentError):
    """خطای اعتبارسنجی کامنت"""
    
    def __init__(self, field_name, error_message):
        self.field_name = field_name
        self.error_message = error_message
        super().__init__(f"خطا در فیلد {field_name}: {error_message}")


class CommentContentTooShortError(CommentValidationError):
    """محتوای کامنت بسیار کوتاه است"""
    
    def __init__(self, min_length):
        super().__init__(
            field_name="content",
            error_message=f"متن نظر باید حداقل شامل {min_length} کاراکتر باشد"
        )


class CommentSpamDetectedError(CommentError):
    """کامنت به عنوان اسپم شناسایی شد"""
    
    def __init__(self, reason=None):
        self.reason = reason
        message = "نظر شما به عنوان اسپم شناسایی شد"
        if reason:
            message += f" (دلیل: {reason})"
        super().__init__(message)


class CommentReplyDepthExceededError(CommentError):
    """حداکثر عمق پاسخ به کامنت رعایت نشده"""
    
    def __init__(self, max_depth):
        super().__init__(
            f"حداکثر عمق پاسخ‌دهی به نظرات {max_depth} سطح می‌باشد"
        )