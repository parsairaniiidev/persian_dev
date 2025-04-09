# core/domain/exceptions.py
from typing import Optional

class DomainException(Exception):
    """کلاس پایه برای تمام خطاهای دامنه"""
    default_message = "A domain error occurred"
    status_code = 400  # HTTP Bad Request by default

    def __init__(self, message=None, details=None, code=None):
        self.message = message or self.default_message
        self.details = details or {}
        self.code = code or self.__class__.__name__.lower()
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

    def to_dict(self):
        """Convert exception to dictionary for API responses"""
        return {
            'error': self.code,
            'message': self.message,
            'details': self.details
        }


class ValidationError(DomainException):
    """When input validation fails"""
    default_message = "Validation error"
    status_code = 422  # HTTP Unprocessable Entity

    def __init__(self, message=None, errors=None, error_code=None):
        super().__init__(message)
        self.error_code = error_code or "validation_error"
        self.errors = errors or {}
        self.details['errors'] = self.errors
        
    @classmethod
    def from_single_error(cls, field, error, code=None):
        return cls(
            message=f"Validation failed for {field}",
            errors={field: [error]},
            error_code=code
        )


class AuthenticationError(DomainException):
    """Base class for all authentication errors"""
    default_message = "Authentication failed"
    status_code = 401  # HTTP Unauthorized


class InvalidCredentialsError(AuthenticationError):
    """When username/password combination is invalid"""
    default_message = "Invalid username or password"
    
    def __init__(self, username=None, message=None):
        self.username = username
        super().__init__(
            message or f"Invalid credentials for user '{username}'" if username else self.default_message,
            code="invalid_credentials"
        )


class AccountLockedError(AuthenticationError):
    """When account is temporarily locked"""
    default_message = "Account temporarily locked"
    
    def __init__(self, username, unlock_at=None, message=None):
        self.username = username
        self.unlock_at = unlock_at  # datetime
        super().__init__(
            message or f"Account locked until {unlock_at}" if unlock_at else self.default_message,
            code="account_locked",
            details={
                'unlock_at': unlock_at.isoformat() if unlock_at else None
            }
        )


class TwoFactorRequiredError(AuthenticationError):
    """When 2FA is required to complete authentication"""
    default_message = "Two-factor authentication required"
    status_code = 403  # HTTP Forbidden
    
    def __init__(self, user_id, methods_available=None, message=None):
        self.user_id = user_id
        self.methods_available = methods_available or ['sms', 'email', 'authenticator']
        super().__init__(
            message or self.default_message,
            code="2fa_required",
            details={
                'user_id': user_id,
                'available_methods': self.methods_available
            }
        )


class TwoFactorError(AuthenticationError):
    """Base class for all 2FA-related errors"""
    default_message = "Two-factor authentication error"
    status_code = 403  # Forbidden


class TwoFactorCodeExpiredError(TwoFactorError):
    """When the 2FA code has expired"""
    default_message = "Two-factor code has expired"
    
    def __init__(self, user_id, code_type, expires_at, message=None):
        self.user_id = user_id
        self.code_type = code_type  # 'sms', 'email', 'totp'
        self.expires_at = expires_at
        super().__init__(
            message or f"{code_type.upper()} code expired at {expires_at}",
            code="2fa_code_expired",
            details={
                'user_id': user_id,
                'code_type': code_type,
                'expires_at': expires_at.isoformat()
            }
        )


class InvalidTwoFactorCodeError(TwoFactorError):
    """When an invalid 2FA code is provided"""
    default_message = "Invalid two-factor code"
    
    def __init__(self, user_id, code_type, attempts_remaining=None, message=None):
        self.user_id = user_id
        self.code_type = code_type
        self.attempts_remaining = attempts_remaining
        super().__init__(
            message or self.default_message,
            code="invalid_2fa_code",
            details={
                'user_id': user_id,
                'code_type': code_type,
                'attempts_remaining': attempts_remaining
            }
        )

    @classmethod
    def with_retry_info(cls, user_id, code_type, max_attempts, attempts_made):
        return cls(
            user_id=user_id,
            code_type=code_type,
            attempts_remaining=max_attempts - attempts_made,
            message=f"Invalid {code_type} code ({max_attempts - attempts_made} attempts remaining)"
        )


class UserNotFoundError(DomainException):
    """Raised when a user cannot be found in the system"""
    default_message = "User not found"
    status_code = 404  # HTTP Not Found
    
    def __init__(self, identifier, message=None, code="user_not_found"):
        self.identifier = identifier  # Could be username, email, or user_id
        super().__init__(
            message or f"User with identifier '{identifier}' not found",
            code=code
        )

    @classmethod
    def by_email(cls, email):
        return cls(email, f"User with email '{email}' not found")

    @classmethod
    def by_id(cls, user_id):
        return cls(user_id, f"User with ID '{user_id}' not found", "user_id_not_found")


class PasswordHashingError(DomainException):
    """Raised when password hashing fails"""
    default_message = "Password hashing error"
    status_code = 500  # HTTP Internal Server Error


class EmailSendingError(DomainException):
    """Exception raised when email sending fails."""
    default_message = "Email sending failed"
    status_code = 502  # HTTP Bad Gateway
    
    def __init__(self, message=None, original_exception=None):
        """
        Args:
            message: Human-readable error message
            original_exception: Original exception that caused this error (optional)
        """
        self.original_exception = original_exception
        details = {
            'original_exception': str(original_exception) if original_exception else None
        }
        super().__init__(message, details=details)


class EmailAlreadyExistsError(DomainException):
    """Error when trying to register with an existing email"""
    default_message = "Email already exists"
    status_code = 409  # HTTP Conflict


class PasswordComplexityError(ValidationError):
    """Error when password doesn't meet complexity requirements"""
    default_message = "Password must be at least 8 characters and contain letters and numbers"
    
    def __init__(self, requirements=None):
        details = {
            'requirements': requirements or {
                'min_length': 8,
                'require_letters': True,
                'require_numbers': True
            }
        }
        super().__init__(self.default_message, details=details)

class SpamDetectionError(Exception):
    """خطای پایه برای تشخیص اسپم"""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        self.original_error = original_error
        super().__init__(message)


class SpamAPILimitError(SpamDetectionError):
    """خطای محدودیت دسترسی به API"""
    pass


class SpamContentAnalyzeError(SpamDetectionError):
    """خطای تحلیل محتوا"""
    pass

class EmailDeliveryError(Exception):
    """خطای پایه برای ارسال ایمیل"""
    
    def __init__(self, message: str, provider: Optional[str] = None):
        self.provider = provider
        super().__init__(message)


class EmailConfigurationError(EmailDeliveryError):
    """خطای تنظیمات سرویس ایمیل"""
    pass


class EmailRateLimitError(EmailDeliveryError):
    """خطای محدودیت نرخ ارسال"""
    pass