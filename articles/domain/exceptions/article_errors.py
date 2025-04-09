class ArticleError(Exception):
    """خطای پایه برای تمام خطاهای مربوط به مقالات"""
    pass


class ArticleNotFoundError(ArticleError):
    """مقاله مورد نظر یافت نشد"""
    
    def __init__(self, article_id=None):
        self.article_id = article_id
        message = "مقاله مورد نظر یافت نشد"
        if article_id:
            message = f"مقاله با شناسه {article_id} یافت نشد"
        super().__init__(message)


class ArticleAlreadyPublishedError(ArticleError):
    """مقاله قبلا منتشر شده است"""
    
    def __init__(self, article_id=None):
        self.article_id = article_id
        message = "مقاله قبلا منتشر شده است"
        if article_id:
            message = f"مقاله با شناسه {article_id} قبلا منتشر شده است"
        super().__init__(message)


class InvalidArticleStatusError(ArticleError):
    """وضعیت مقاله نامعتبر است"""
    
    def __init__(self, current_status, expected_status=None):
        self.current_status = current_status
        self.expected_status = expected_status
        message = f"وضعیت فعلی مقاله ({current_status}) نامعتبر است"
        if expected_status:
            message += f"، وضعیت مورد انتظار: {expected_status}"
        super().__init__(message)


class ArticlePermissionError(ArticleError):
    """دسترسی به مقاله مجاز نیست"""
    
    def __init__(self, user_id=None, article_id=None):
        self.user_id = user_id
        self.article_id = article_id
        message = "دسترسی به این مقاله مجاز نیست"
        if user_id and article_id:
            message = f"کاربر با شناسه {user_id} اجازه دسترسی به مقاله {article_id} را ندارد"
        super().__init__(message)


class ArticleValidationError(ArticleError):
    """خطای اعتبارسنجی مقاله"""
    
    def __init__(self, field_name, error_message):
        self.field_name = field_name
        self.error_message = error_message
        super().__init__(f"خطا در فیلد {field_name}: {error_message}")


class ArticleContentTooShortError(ArticleValidationError):
    """محتوای مقاله بسیار کوتاه است"""
    
    def __init__(self, min_length):
        super().__init__(
            field_name="content",
            error_message=f"محتوای مقاله باید حداقل شامل {min_length} کاراکتر باشد"
        )


class ArticleTitleDuplicateError(ArticleValidationError):
    """عنوان مقاله تکراری است"""
    
    def __init__(self, title):
        super().__init__(
            field_name="title",
            error_message=f"مقاله با عنوان '{title}' از قبل وجود دارد"
        )