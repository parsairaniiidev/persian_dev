from dataclasses import dataclass

@dataclass
class NotificationData:
    title: str
    content: str
    metadata: dict = None