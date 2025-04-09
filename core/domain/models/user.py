# core/domain/models/user.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.domain.value_objects.email import Email
from core.domain.models.role import Role
from core.infrastructure.security.password_hasher import AdvancedPasswordHasher

class UserManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields):
        """
        ایجاد کاربر معمولی با ایمیل و رمز عبور
        """
        if not email:
            raise ValidationError("ایمیل الزامی است")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        ایجاد کاربر مدیریتی
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='نام کاربری',
        help_text='حداکثر 50 کاراکتر'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='آدرس ایمیل',
        error_messages={
            'unique': 'این ایمیل قبلا ثبت شده است'
        }
    )
    password_hash = models.CharField(
        max_length=128,
        verbose_name='رمز عبور هش شده'
    )
    roles = models.ManyToManyField(
        Role,
        blank=True,
        verbose_name='نقش‌های کاربر'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='فعال'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='کاربر مدیریت'
    )
    failed_login_attempts = models.IntegerField(
        default=0,
        verbose_name='تعداد تلاش ناموفق'
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='آخرین ورود'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        indexes = [
            models.Index(fields=['email'], name='email_index'),
            models.Index(fields=['username'], name='username_index'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"

    def set_password(self, raw_password):
        """
        تنظیم رمز عبور با هش کردن آن
        """
        self.password_hash = AdvancedPasswordHasher().hash_password(raw_password)
        self.save(update_fields=['password_hash'])

    def check_password(self, raw_password):
        """
        بررسی تطابق رمز عبور
        """
        return AdvancedPasswordHasher().verify_password(raw_password, self.password_hash)

    def activate(self):
        """
        فعالسازی حساب کاربری
        """
        self.is_active = True
        self.save(update_fields=['is_active'])

    def deactivate(self):
        """
        غیرفعالسازی حساب کاربری
        """
        self.is_active = False
        self.save(update_fields=['is_active'])

    def increment_failed_attempts(self):
        """
        افزایش تعداد تلاش‌های ناموفق ورود
        """
        self.failed_login_attempts = models.F('failed_login_attempts') + 1
        self.save(update_fields=['failed_login_attempts'])

    def reset_failed_attempts(self):
        """
        بازنشانی تعداد تلاش‌های ناموفق
        """
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])

    def update_last_login(self):
        """
        بروزرسانی زمان آخرین ورود
        """
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True