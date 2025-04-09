from datetime import datetime, timedelta
from typing import Dict, List, Optional
from domain.models.article import Article
from application.interfaces.repositories.article_repository import ArticleRepository
from application.interfaces.repositories.comment_repository import CommentRepository
from application.interfaces.services.statistics_service import StatisticsService

class ArticleStatistics:
    """سرویس آمار و تحلیل مقالات"""
    
    def __init__(
        self,
        article_repo: ArticleRepository,
        comment_repo: CommentRepository,
        stats_service: StatisticsService
    ):
        self.article_repo = article_repo
        self.comment_repo = comment_repo
        self.stats_service = stats_service

    def get_article_engagement(self, article_id: str) -> Dict:
        """
        محاسبه میزان تعامل با مقاله
        Args:
            article_id: شناسه مقاله
        Returns:
            Dict: آمار تعامل
        """
        article = self.article_repo.get_by_id(article_id)
        if not article:
            return {}
        
        stats = self.stats_service.get_article_stats(article_id)
        comment_count = self.comment_repo.count_by_article(article_id)
        
        return {
            'article_id': article_id,
            'view_count': stats.get('view_count', 0),
            'comment_count': comment_count,
            'average_read_time': stats.get('average_read_time', 0),
            'engagement_score': self._calculate_engagement_score(
                stats.get('view_count', 0),
                comment_count,
                stats.get('average_read_time', 0)
            ),
            'last_updated': datetime.now().isoformat()
        }

    def get_author_performance(self, author_id: str) -> Dict:
        """
        تحلیل عملکرد نویسنده
        Args:
            author_id: شناسه نویسنده
        Returns:
            Dict: آمار عملکرد
        """
        articles = self.article_repo.get_by_author(author_id)
        stats = {
            'total_articles': len(articles),
            'published_articles': 0,
            'total_views': 0,
            'total_comments': 0,
            'articles': []
        }
        
        for article in articles:
            if article.status == 'published':
                stats['published_articles'] += 1
            
            article_stats = self.stats_service.get_article_stats(article.id)
            comment_count = self.comment_repo.count_by_article(article.id)
            
            stats['total_views'] += article_stats.get('view_count', 0)
            stats['total_comments'] += comment_count
            
            stats['articles'].append({
                'article_id': article.id,
                'title': article.title,
                'views': article_stats.get('view_count', 0),
                'comments': comment_count,
                'published_at': article.published_at.isoformat() if article.published_at else None
            })
        
        return stats

    def get_category_analytics(self, category_id: str) -> Dict:
        """
        تحلیل آمار یک دسته‌بندی
        Args:
            category_id: شناسه دسته‌بندی
        Returns:
            Dict: آمار دسته‌بندی
        """
        articles = self.article_repo.get_by_category(category_id)
        stats = {
            'total_articles': len(articles),
            'total_views': 0,
            'total_comments': 0,
            'trending_articles': [],
            'last_updated': datetime.now().isoformat()
        }
        
        for article in articles:
            article_stats = self.stats_service.get_article_stats(article.id)
            comment_count = self.comment_repo.count_by_article(article.id)
            
            stats['total_views'] += article_stats.get('view_count', 0)
            stats['total_comments'] += comment_count
            
            stats['trending_articles'].append({
                'article_id': article.id,
                'title': article.title,
                'views': article_stats.get('view_count', 0),
                'comments': comment_count
            })
        
        # مرتب‌سازی مقالات پرطرفدار
        stats['trending_articles'].sort(key=lambda x: x['views'], reverse=True)
        stats['trending_articles'] = stats['trending_articles'][:5]
        
        return stats

    def _calculate_engagement_score(
        self,
        views: int,
        comments: int,
        avg_read_time: float
    ) -> float:
        """
        محاسبه نمره تعامل مقاله
        Args:
            views: تعداد بازدیدها
            comments: تعداد نظرات
            avg_read_time: میانگین زمان مطالعه (ثانیه)
        Returns:
            float: نمره تعامل
        """
        # وزن‌دهی عوامل مختلف
        view_weight = 0.4
        comment_weight = 0.3
        read_time_weight = 0.3
        
        # نرمالایز کردن مقادیر
        normalized_views = min(views / 1000, 1.0)  # حداکثر 1000 بازدید
        normalized_comments = min(comments / 50, 1.0)  # حداکثر 50 کامنت
        normalized_read_time = min(avg_read_time / 300, 1.0)  # حداکثر 5 دقیقه
        
        return (
            (normalized_views * view_weight) +
            (normalized_comments * comment_weight) +
            (normalized_read_time * read_time_weight)
        ) * 100  # تبدیل به درصد