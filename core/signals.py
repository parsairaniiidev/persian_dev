from django.db.models.signals import post_save
from django.dispatch import receiver
from core.domain.models.user import User
from core.infrastructure.services.email.sendgrid_email_service import SendgridEmailService

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    ارسال ایمیل خوشامدگویی پس از ثبت‌نام کاربر جدید
    """
    if created and instance.email:
        email_service = SendgridEmailService()
        email_service.send(
            to=instance.email,
            subject="خوش آمدید به سامانه ما",
            template="welcome_email",
            context={'username': instance.username}
        )