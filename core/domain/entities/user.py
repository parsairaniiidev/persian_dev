from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from core.domain.value_objects.email import Email, UserId

@dataclass
class User:
    """User domain entity"""
    id: UserId
    email: Email
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    two_factor_enabled: bool = False
    metadata: Dict = None

    def __post_init__(self):
        self.metadata = self.metadata or {}
        if 'date_joined' not in self.metadata:
            self.metadata['date_joined'] = datetime.utcnow()

    @classmethod
    def create(
        cls,
        email: str,
        password_hash: str,
        first_name: str = "",
        last_name: str = ""
    ) -> 'User':
        """Factory method for creating new users"""
        return cls(
            id=UserId.generate(),
            email=Email(email),
            first_name=first_name,
            last_name=last_name,
            hashed_password=password_hash,
            metadata={
                'date_joined': datetime.utcnow()
            }
        )

    def verify_email(self):
        """Mark email as verified"""
        self.is_verified = True

    def enable_2fa(self):
        """Enable two-factor authentication"""
        self.two_factor_enabled = True

    def update_password(self, new_hash: str):
        """Update password hash"""
        self.hashed_password = new_hash
        self.metadata['last_password_change'] = datetime.utcnow()

    def get_full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id