import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass
from core.domain.exceptions import EmailDeliveryError

logger = logging.getLogger(__name__)

@dataclass
class EmailMessage:
    to: str | list[str]
    subject: str
    body: str
    cc: Optional[list[str]] = None
    bcc: Optional[list[str]] = None
    attachments: Optional[list[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseEmailProvider(ABC):
    """رابطه پایه برای تمام ارائه‌دهندگان سرویس ایمیل"""

    def __init__(self, api_key: Optional[str] = None):
        self._api_key = api_key
        self._setup_provider()

    @abstractmethod
    def _setup_provider(self) -> None:
        """تنظیمات اولیه اتصال به سرویس ایمیل"""
        pass

    @abstractmethod
    def _send_email(self, message: EmailMessage) -> bool:
        """ارسال واقعی ایمیل (پیاده‌سازی خاص هر سرویس)"""
        pass

    def send_email(self, message: EmailMessage) -> bool:
        """
        ارسال ایمیل با مدیریت خطاها و لاگ‌گیری
        """
        try:
            logger.debug(f"Attempting to send email to {message.to}")
            
            if not message.to:
                raise ValueError("Recipient address cannot be empty")
                
            result = self._send_email(message)
            
            logger.info(
                f"Email successfully sent to {message.to}. "
                f"Subject: {message.subject}"
            )
            return result
            
        except Exception as e:
            logger.error(f"Failed to send email to {message.to}: {str(e)}")
            raise EmailDeliveryError(f"Email delivery failed: {str(e)}")

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """نام ارائه‌دهنده سرویس"""
        pass


class SMTPEmailProvider(BaseEmailProvider):
    """
    پیاده‌سازی ارسال ایمیل از طریق SMTP
    
    پارامترها:
        host: آدرس سرور SMTP
        port: پورت سرور
        username: نام کاربری
        password: رمز عبور
        use_tls: استفاده از TLS
        timeout: زمان انتظار (ثانیه)
    """

    def __init__(
        self,
        host: str,
        port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
        timeout: int = 10,
        **kwargs
    ):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._use_tls = use_tls
        self._timeout = timeout
        super().__init__(**kwargs)

    def _setup_provider(self) -> None:
        """تنظیمات اتصال SMTP"""
        import smtplib
        self._smtp_class = smtplib.SMTP
        logger.info(f"Initialized SMTP provider for {self._host}:{self._port}")

    def _send_email(self, message: EmailMessage) -> bool:
        """پیاده‌سازی ارسال از طریق SMTP"""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        msg = MIMEMultipart()
        msg['From'] = self._username
        msg['To'] = message.to if isinstance(message.to, str) else ', '.join(message.to)
        msg['Subject'] = message.subject
        
        if message.cc:
            msg['Cc'] = ', '.join(message.cc)
            
        msg.attach(MIMEText(message.body, 'plain'))
        
        try:
            with self._smtp_class(
                host=self._host,
                port=self._port,
                timeout=self._timeout
            ) as server:
                if self._use_tls:
                    server.starttls()
                
                if self._username and self._password:
                    server.login(self._username, self._password)
                
                recipients = [message.to] if isinstance(message.to, str) else message.to
                if message.cc:
                    recipients.extend(message.cc)
                
                server.sendmail(
                    from_addr=self._username,
                    to_addrs=recipients,
                    msg=msg.as_string()
                )
                return True
        except Exception as e:
            logger.error(f"SMTP send failed: {str(e)}")
            raise

    @property
    def provider_name(self) -> str:
        return "SMTPEmailProvider"


class SendGridEmailProvider(BaseEmailProvider):
    """پیاده‌سازی ارسال ایمیل از طریق SendGrid"""

    def __init__(self, api_key: str, **kwargs):
        self._api_key = api_key
        super().__init__(api_key=api_key, **kwargs)

    def _setup_provider(self) -> None:
        """تنظیمات اتصال به SendGrid"""
        try:
            from sendgrid import SendGridAPIClient
            self._client = SendGridAPIClient(self._api_key)
            logger.info("Initialized SendGrid email provider")
        except ImportError:
            raise RuntimeError("SendGrid library not installed. Use `pip install sendgrid`")

    def _send_email(self, message: EmailMessage) -> bool:
        """پیاده‌سازی ارسال از طریق SendGrid"""
        from sendgrid.helpers.mail import Mail, Email, To, Content
        
        from_email = Email(self._username or "no-reply@example.com")
        to_email = To(message.to)
        content = Content("text/plain", message.body)
        
        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=message.subject,
            plain_text_content=content
        )
        
        response = self._client.send(mail)
        return response.status_code == 202

    @property
    def provider_name(self) -> str:
        return "SendGridEmailProvider"