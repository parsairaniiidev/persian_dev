from typing import Optional
from datetime import datetime
from domain.models.article import Article
from application.interfaces.services.search_service import SearchService
from application.interfaces.repositories.article_repository import ArticleRepository
from infrastructure.event_handlers.article_events import ArticlePublishedEvent, ArticleUpdatedEvent

class ArticleIndexer:
    """سرویس ایندکس کردن مقالات در موتور جستجو"""
    
    def __init__(
        self,
        search_service: SearchService,
        article_repository: ArticleRepository
    ):
        self.search_service = search_service
        self.article_repository = article_repository

    def handle_article_published(self, event: ArticlePublishedEvent) -> bool:
        """
        ایندکس کردن مقاله پس از انتشار
        Args:
            event: رویداد انتشار مقاله
        Returns:
            bool: نتیجه عملیات
        """
        article = self.article_repository.get_by_id(event.article_id)
        if not article:
            return False
        
        return self.search_service.index_article(article)

    def handle_article_updated(self, event: ArticleUpdatedEvent) -> bool:
        """
        به‌روزرسانی مقاله در موتور جستجو
        Args:
            event: رویداد به‌روزرسانی مقاله
        Returns:
            bool: نتیجه عملیات
        """
        article = self.article_repository.get_by_id(event.article_id)
        if not article:
            return False
        
        return self.search_service.update_indexed_article(article)

    def index_existing_articles(self, batch_size: int = 100) -> dict:
        """
        ایندکس کردن تمام مقالات موجود در دیتابیس
        Args:
            batch_size: تعداد مقالات در هر بسته
        Returns:
            dict: آمار عملیات
        """
        stats = {
            'total_indexed': 0,
            'start_time': datetime.now(),
            'end_time': None,
            'success': True
        }
        
        page = 1
        while True:
            articles = self.article_repository.get_all_published(page, batch_size)
            if not articles:
                break
            
            for article in articles:
                try:
                    if self.search_service.index_article(article):
                        stats['total_indexed'] += 1
                except Exception as e:
                    stats['success'] = False
                    # ادامه عملیات با وجود خطا
            
            page += 1
        
        stats['end_time'] = datetime.now()
        return stats