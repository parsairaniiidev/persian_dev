from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta
from domain.models.article import Article

class StatisticsService(ABC):
    """اینترفیس سرویس آمار و گزارشات"""
    
    @abstractmethod
    def record_article_view(self, article_id: str) -> bool:
        """ثبت بازدید یک مقاله"""
        pass
    
    @abstractmethod
    def record_search(self, query: str, result_count: int) -> bool:
        """ثبت آمار جستجو"""
        pass
    
    @abstractmethod
    def get_article_stats(self, article_id: str) -> dict:
        """دریافت آمار یک مقاله"""
        pass
    
    @abstractmethod
    def get_popular_articles(
        self,
        time_range: str = 'week',
        limit: int = 5
    ) -> List[dict]:
        """
        دریافت پر بازدیدترین مقالات در بازه زمانی
        
        Args:
            time_range: بازه زمانی (day/week/month/year/all)
            limit: تعداد مقالات
        """
        pass
    
    @abstractmethod
    def get_author_stats(self, author_id: str) -> dict:
        """دریافت آمار یک نویسنده"""
        pass
    
    @abstractmethod
    def get_category_stats(self, category_id: str) -> dict:
        """دریافت آمار یک دسته‌بندی"""
        pass
    
    @abstractmethod
    def get_site_stats(self) -> dict:
        """دریافت آمار کلی سایت"""
        pass
    
    @abstractmethod
    def get_search_trends(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[dict]:
        """دریافت روندهای جستجو"""
        pass
    
    @abstractmethod
    def get_comment_stats(self, article_id: Optional[str] = None) -> dict:
        """دریافت آمار نظرات"""
        pass