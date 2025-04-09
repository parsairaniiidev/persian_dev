# domain/repositories/search_log_repository.py
from abc import ABC, abstractmethod
from domain.entities.search_log import SearchLog
from typing import List

class SearchLogRepository(ABC):
    """Interface for search log persistence"""
    
    @abstractmethod
    def log_search(self, search_log: SearchLog) -> None:
        """Persist a search log entry"""
        pass
    
    @abstractmethod
    def get_recent_searches(self, user_id: str, limit: int = 10) -> List[SearchLog]:
        """Retrieve recent searches for a user"""
        pass
    
    @abstractmethod
    def get_popular_searches(self, limit: int = 10) -> List[str]:
        """Get most popular search queries"""
        pass