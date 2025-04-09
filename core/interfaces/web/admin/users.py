# core/interfaces/web/admin/users.py
from django.contrib import admin
from core.domain.models.user import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    پنل مدیریت کاربران در ادمین جنگو
    """
    list_display = ('username', 'email', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Permissions', {'fields': ('is_active', 'roles')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    def activate_users(self, request, queryset):
        """اکشن سفارشی برای فعالسازی کاربران"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} کاربر فعال شدند")
    
    actions = [activate_users]