from django.apps import AppConfig

class CoreConfig(AppConfig):
    """
    پیکربندی اصلی ماژول Core
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """
        اجرای کدهای هنگام بارگذاری اپلیکیشن
        """
        # ایمپورت سیگنال‌ها
        import core.signals