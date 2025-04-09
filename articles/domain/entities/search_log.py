# domain/entities/search_log.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SearchLog:
    """Domain entity representing a search log entry"""
    query: str
    timestamp: datetime
    user_id: Optional[str] = None
    results_count: int = 0
    metadata: dict = None  # Additional search context data

    def __init__(self, query: str, user_id: str = None, metadata: dict = None):
        self.query = query
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.metadata = metadata or {}