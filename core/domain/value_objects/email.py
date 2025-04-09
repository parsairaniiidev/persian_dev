import re
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Email:
    """Email value object with validation"""
    address: str

    def __post_init__(self):
        if not self.is_valid():
            raise ValueError(f"Invalid email address: {self.address}")

    def is_valid(self) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, self.address) is not None

    def get_domain(self) -> str:
        return self.address.split('@')[-1]

    def __str__(self):
        return self.address


@dataclass(frozen=True)
class UserId:
    """User ID value object"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("User ID cannot be empty")

    def __str__(self):
        return self.value

    @classmethod
    def generate(cls):
        """Factory method for generating new IDs"""
        import uuid
        return cls(str(uuid.uuid4()))