from django.db import models
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from application.interfaces.services.statistics_service import StatisticsService
from articles.domain.models.search import DjangoSearchLog
from domain.entities.article_stats import ArticleStats

class DjangoStatisticsService(StatisticsService):
    """پیاده‌سازی سرویس آمار با استفاده از Django ORM"""
    
    def record_article_view(self, article_id: str) -> bool:
        try:
            stats, created = ArticleStats.objects.get_or_create(
                article_id=article_id,
                date=datetime.now().date()
            )
            stats.view_count = models.F('view_count') + 1
            stats.save()
            return True
        except Exception:
            return False

    def record_search(self, query: str, result_count: int) -> bool:
        try:
            DjangoSearchLog.objects.create(
                query=query,
                result_count=result_count,
                timestamp=datetime.now()
            )
            return True
        except Exception:
            return False

    def get_article_stats(self, article_id: str) -> Dict:
        stats = ArticleStats.objects.filter(article_id=article_id)
        
        total_views = stats.aggregate(models.Sum('view_count'))['view_count__sum'] or 0
        avg_read_time = stats.aggregate(models.Avg('read_time'))['read_time__avg'] or 0
        
        return {
            'total_views': total_views,
            'average_read_time': avg_read_time,
            'daily_stats': [
                {'date': s.date, 'views': s.view_count}
                for s in stats.order_by('-date')[:30]
            ]
        }

    # سایر متدهای StatisticsService...