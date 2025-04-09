from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

@dataclass
class Notification:
    id: str
    title: str
    content: str
    created_at: datetime
    is_read: bool = False

    def __init__(self, title: str, content: str):
        self.id = str(uuid4())
        self.title = title
        self.content = content
        self.created_at = datetime.now()