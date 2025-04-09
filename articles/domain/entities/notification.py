# domain/entities/notification.py
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Optional, Dict

@dataclass
class Notification:
    """Entity representing a notification"""
    id: str
    title: str
    content: str
    created_at: datetime
    metadata: Optional[Dict] = None
    is_read: bool = False

    def __init__(self, title: str, content: str, metadata: Optional[Dict] = None):
        self.id = str(uuid4())
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.metadata = metadata or {}