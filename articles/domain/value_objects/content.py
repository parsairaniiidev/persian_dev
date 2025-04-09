# domain/value_objects/content.py
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Content:
    """Value object representing content that can be analyzed"""
    text: str
    language: str = "fa"
    metadata: Optional[Dict[str, str]] = None