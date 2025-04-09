from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Optional, Literal, Any



@dataclass
class DomainEvent:
    """Base class for all domain events"""
    event_id: str
    occurred_on: datetime
    version: int = 1

    def __init__(self):
        self.event_id = self._generate_event_id()
        self.occurred_on = datetime.utcnow()

    def _generate_event_id(self) -> str:
        return f"{self.__class__.__name__}-{uuid.uuid4()}"
    
@dataclass
class UserLoggedInEvent(DomainEvent):
    """Emitted when a user successfully logs in"""
    user_id: str
    ip_address: str
    user_agent: str
    login_method: Literal["password", "sso", "magic_link"]
    is_2fa_used: bool = False
    device_id: Optional[str] = None
    session_id: Optional[str] = None

    @property
    def is_suspicious(self) -> bool:
        """Detects potentially suspicious logins"""
        return (
            self.login_method == "password" 
            and not self.is_2fa_used
            and not self.device_id
        )

    def to_audit_log(self) -> dict:
        return {
            "event_type": "user_login",
            "user_id": self.user_id,
            "timestamp": self.occurred_on.isoformat(),
            "metadata": {
                "ip": self.ip_address,
                "method": self.login_method,
                "device": self.device_id
            }
        }


@dataclass
class UserRegisteredEvent:
    user_id: int
    registration_date: datetime
    source_ip: str

@dataclass
class PasswordChangedEvent(DomainEvent):
    """Raised when a user changes their password"""
    user_id: str
    changed_at: datetime
    is_forced_reset: bool = False
    metadata: dict = None

    def __post_init__(self):
        super().__init__()
        if not self.metadata:
            self.metadata = {}

    def to_dict(self):
        return {
            "event_type": "password_changed",
            "user_id": self.user_id,
            "is_forced": self.is_forced_reset,
            "timestamp": self.occurred_on.isoformat()
        }


@dataclass
class ProfileUpdatedEvent(DomainEvent):
    """Raised when user profile is updated"""
    user_id: str
    updated_fields: dict  # e.g. {'email': 'old@new.com', 'name': 'Old → New'}
    previous_values: dict
    updated_by: str  # Could be 'user' or 'admin'

    @property
    def has_sensitive_changes(self) -> bool:
        sensitive_fields = {'email', 'phone'}
        return bool(sensitive_fields & set(self.updated_fields.keys()))