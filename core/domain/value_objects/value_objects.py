from dataclasses import dataclass
from typing import Optional

@dataclass
class Content:
    """شیء ارزش برای محتوای قابل تحلیل"""
    id: str
    text: str
    language: str = "fa"
    author_id: Optional[str] = None
    metadata: Optional[dict] = None