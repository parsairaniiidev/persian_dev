# core/application/interfaces/repositories/role_repository.py
from abc import ABC, abstractmethod
from typing import List
from core.domain.models.role import Role

class IRoleRepository(ABC):
    """
    اینترفیس مخزن نقش‌های کاربری
    """
    @abstractmethod
    def get_user_roles(self, user_id: int) -> List[Role]:
        pass
    
    @abstractmethod
    def assign_role(self, user_id: int, role_name: str) -> None:
        pass
    
    @abstractmethod
    def revoke_role(self, user_id: int, role_name: str) -> None:
        pass