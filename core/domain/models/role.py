# core/domain/models/role.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from typing import List, Optional

class Role(models.Model):
    """
    مدل نقش کاربری با دسترسی‌های مختلف
    شامل سیستم مدیریت دسترسی پیشرفته با اعتبارسنجی‌های جامع
    """
    class PermissionGroups(models.TextChoices):
        USER = 'user', _('مدیریت کاربران')
        CONTENT = 'content', _('مدیریت محتوا')
        SYSTEM = 'system', _('تنظیمات سیستم')
        REPORT = 'report', _('گزارشات')
        FINANCE = 'finance', _('مالی')

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('نام نقش'),
        help_text=_('نام یکتا برای نقش (حداکثر 50 کاراکتر)'),
        error_messages={
            'unique': _('این نام نقش قبلا ثبت شده است')
        }
    )
    
    permissions = models.JSONField(
        default=list,
        verbose_name=_('دسترسی‌ها'),
        help_text=_('لیست دسترسی‌های این نقش به صورت JSON')
    )
    
    permission_group = models.CharField(
        max_length=20,
        choices=PermissionGroups.choices,
        default=PermissionGroups.USER,
        verbose_name=_('گروه دسترسی')
    )
    
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('نقش پیش‌فرض'),
        help_text=_('آیا این نقش به صورت پیش‌فرض به کاربران جدید اختصاص داده شود؟')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ ایجاد')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاریخ بروزرسانی')
    )

    class Meta:
        verbose_name = _('نقش')
        verbose_name_plural = _('نقش‌ها')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_role_name'
            ),
            models.UniqueConstraint(
                fields=['is_default'],
                condition=models.Q(is_default=True),
                name='unique_default_role'
            )
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """
        اعتبارسنجی مدل قبل از ذخیره‌سازی
        """
        super().clean()
        
        if not isinstance(self.permissions, list):
            raise ValidationError({
                'permissions': _('دسترسی‌ها باید به صورت لیست باشند')
            })
            
        for perm in self.permissions:
            if not isinstance(perm, str):
                raise ValidationError({
                    'permissions': _('هر دسترسی باید یک رشته متنی باشد')
                })

    def save(self, *args, **kwargs):
        """
        ذخیره مدل با اعمال اعتبارسنجی‌ها
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def add_permission(self, permission: str) -> bool:
        """
        افزودن دسترسی جدید به نقش
        
        Args:
            permission: نام دسترسی مورد نظر
            
        Returns:
            bool: True اگر دسترسی اضافه شد، False اگر از قبل وجود داشت
        """
        if permission not in self.permissions:
            self.permissions.append(permission)
            self.save(update_fields=['permissions'])
            return True
        return False

    def remove_permission(self, permission: str) -> bool:
        """
        حذف دسترسی از نقش
        
        Args:
            permission: نام دسترسی مورد نظر
            
        Returns:
            bool: True اگر دسترسی حذف شد، False اگر وجود نداشت
        """
        if permission in self.permissions:
            self.permissions.remove(permission)
            self.save(update_fields=['permissions'])
            return True
        return False

    def has_permission(self, permission: str) -> bool:
        """
        بررسی وجود یک دسترسی در نقش
        
        Args:
            permission: نام دسترسی مورد بررسی
            
        Returns:
            bool: True اگر دسترسی وجود دارد
        """
        return permission in self.permissions

    def set_default(self) -> None:
        """
        تنظیم این نقش به عنوان نقش پیش‌فرض
        (به طور خودکار نقش پیش‌فرض قبلی را غیرفعال می‌کند)
        """
        Role.objects.filter(is_default=True).update(is_default=False)
        self.is_default = True
        self.save(update_fields=['is_default'])

    def get_permissions_by_group(self) -> List[str]:
        """
        دریافت دسترسی‌های فیلتر شده بر اساس گروه
        
        Returns:
            List[str]: لیست دسترسی‌های مرتبط با گروه این نقش
        """
        return [p for p in self.permissions if p.startswith(self.permission_group + '.')]

    @classmethod
    def get_default_role(cls) -> Optional['Role']:
        """
        دریافت نقش پیش‌فرض سیستم
        
        Returns:
            Optional[Role]: نقش پیش‌فرض یا None اگر وجود نداشته باشد
        """
        return cls.objects.filter(is_default=True).first()