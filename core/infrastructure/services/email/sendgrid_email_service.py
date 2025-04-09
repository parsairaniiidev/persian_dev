# core/infrastructure/services/email/sendgrid_email_service.py
import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings
from core.application.interfaces.services.email_service import IEmailService

class SendgridEmailService(IEmailService):
    """
    پیاده‌سازی سرویس ایمیل با SendGrid
    """
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    
    def send(self, to: str, subject: str, template: str, context: dict) -> bool:
        """ارسال ایمیل با تمپلیت"""
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=to,
            subject=subject
        )
        message.template_id = template
        message.dynamic_template_data = context
        
        try:
            response = self.sg.send(message)
            return response.status_code == 202
        except Exception as e:
            # لاگ خطا
            return False
    
    def send_verification_email(self, email: str, token: str) -> bool:
        """ارسال ایمیل تأیید حساب"""
        return self.send(
            to=email,
            subject="تأیید ایمیل حساب کاربری",
            template=settings.SENDGRID_VERIFICATION_TEMPLATE_ID,
            context={
                'verification_url': f"{settings.FRONTEND_URL}/verify-email?token={token}"
            }
        )