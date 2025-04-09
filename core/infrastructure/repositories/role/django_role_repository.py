# core/infrastructure/repositories/role/django_role_repository.py
from core.domain.models.role import Role
from core.application.interfaces.repositories.role_repository import IRoleRepository

class DjangoRoleRepository(IRoleRepository):
    """
    پیاده‌سازی مخزن نقش‌ها با Django ORM
    """
    def get_default_role(self) -> Role:
        return Role.objects.filter(is_default=True).first()
    
    def find_by_name(self, name: str) -> Role:
        try:
            return Role.objects.get(name=name)
        except Role.DoesNotExist:
            return None
    
    def create_role(self, name: str, permissions: list) -> Role:
        return Role.objects.create(
            name=name,
            permissions=permissions
        )