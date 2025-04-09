from abc import ABC, abstractmethod
from core.domain.entities.user import User
from core.domain.value_objects.email import UserId, Email

class UserRepository(ABC):
    """Abstract base class for user repositories"""
    
    @abstractmethod
    def get(self, user_id: UserId) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_email(self, email: Email) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, user_id: UserId):
        raise NotImplementedError