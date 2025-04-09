# core/application/interfaces/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from core.domain.models.user import User

class IUserRepository(ABC):
    """
    اینترفیس مخزن کاربر با عملیات پایه
    """
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def update(self, user: User) -> None:
        pass