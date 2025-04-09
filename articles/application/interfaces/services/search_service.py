from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from domain.models.article import Article

@dataclass
class SearchResult:
    """نتیجه جستجو"""
    articles: List[Article]
    total_results: int
    page: int
    page_size: int

class SearchService(ABC):
    """اینترفیس سرویس جستجوی مقالات"""
    
    @abstractmethod
    def search_articles(
        self,
        query: str,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[dict] = None,
        sort_by: Optional[str] = None
    ) -> SearchResult:
        """
        جستجوی مقالات با قابلیت فیلتر و مرتب‌سازی
        
        Args:
            query: عبارت جستجو
            page: شماره صفحه
            page_size: تعداد نتایج در هر صفحه
            filters: فیلترهای جستجو (مثلا {'status': 'published', 'author_id': '...'})
            sort_by: فیلد مرتب‌سازی (مثلا 'newest', 'popular')
            
        Returns:
            SearchResult: نتیجه جستجو
        """
        pass
    
    @abstractmethod
    def index_article(self, article: Article) -> bool:
        """ایندکس کردن مقاله در موتور جستجو"""
        pass
    
    @abstractmethod
    def update_indexed_article(self, article: Article) -> bool:
        """به‌روزرسانی مقاله در موتور جستجو"""
        pass
    
    @abstractmethod
    def remove_article_from_index(self, article_id: str) -> bool:
        """حذف مقاله از موتور جستجو"""
        pass
    
    @abstractmethod
    def get_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """دریافت پیشنهادات جستجو"""
        pass
    
    @abstractmethod
    def get_related_articles(self, article_id: str, limit: int = 5) -> List[Article]:
        """دریافت مقالات مرتبط"""
        pass
    
    @abstractmethod
    def rebuild_index(self) -> bool:
        """بازسازی کامل ایندکس"""
        pass