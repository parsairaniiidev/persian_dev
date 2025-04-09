# infrastructure/repositories/django_search_log_repository.py
from datetime import timedelta
from django.utils import timezone
from domain.repositories.search_log_repository import SearchLogRepository
from domain.entities.search_log import SearchLog
from domain.models.search import DjangoSearchLog  # Your Django model
from typing import List
from django.db import models

class DjangoSearchLogRepository(SearchLogRepository):
    """Django ORM implementation of SearchLogRepository"""
    
    def log_search(self, search_log: SearchLog) -> None:
        """Save search log using Django ORM"""
        DjangoSearchLog.objects.create(
            query=search_log.query,
            user_id=search_log.user_id,
            timestamp=search_log.timestamp,
            metadata=search_log.metadata,
            results_count=search_log.results_count
        )
    
    def get_recent_searches(self, user_id: str, limit: int = 10) -> List[SearchLog]:
        """Get user's recent searches"""
        logs = DjangoSearchLog.objects.filter(
            user_id=user_id
        ).order_by('-timestamp')[:limit]
        
        return [
            SearchLog(
                query=log.query,
                user_id=log.user_id,
                metadata=log.metadata
            ) for log in logs
        ]
    
    def get_popular_searches(self, limit: int = 10) -> List[str]:
        """Get popular searches from last 7 days"""
        since = timezone.now() - timedelta(days=7)
        popular = DjangoSearchLog.objects.filter(
            timestamp__gte=since
        ).values('query').annotate(
            count=models.Count('query')
        ).order_by('-count')[:limit]
        
        return [item['query'] for item in popular]