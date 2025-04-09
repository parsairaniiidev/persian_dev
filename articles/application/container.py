# application/container.py
from dependency_injector import containers, providers
from infrastructure.services.spam_detection import SimpleSpamDetectionService
from infrastructure.services.notification import EmailNotificationService
from infrastructure.external_services.email_provider import SMTPEmailProvider

class ServiceContainer(containers.DeclarativeContainer):
    """Dependency injection container for services"""
    
    # Spam detection configuration
    spam_detection = providers.Singleton(
        SimpleSpamDetectionService,
        spam_keywords=[
            'خرید', 'فوری', 'تخفیف', 'ویزا', 'ارز',
            'کلیک کنید', 'رایگان', 'سود', 'پول'
        ]
    )
    
    # Email provider configuration
    email_provider = providers.Singleton(
        SMTPEmailProvider,
        host="smtp.example.com",
        port=587,
        username="noreply@example.com",
        password="password123"
    )
    
    # Notification service
    notification = providers.Singleton(
        EmailNotificationService,
        email_provider=email_provider
    )