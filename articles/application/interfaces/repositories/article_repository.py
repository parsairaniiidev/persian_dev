from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.article import Article
from core.domain.models.user import User
from domain.value_objects.article_status import ArticleStatus

class ArticleRepository(ABC):
    """اینترفیس ریپازیتوری برای مدیریت مقالات"""
    
    @abstractmethod
    def get_by_id(self, article_id: str) -> Optional[Article]:
        """یافتن مقاله بر اساس شناسه"""
        pass
    
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Article]:
        """یافتن مقاله بر اساس slug"""
        pass
    
    @abstractmethod
    def save(self, article: Article) -> Article:
        """ذخیره یا به‌روزرسانی مقاله"""
        pass
    
    @abstractmethod
    def delete(self, article_id: str) -> bool:
        """حذف مقاله"""
        pass
    
    @abstractmethod
    def exists_by_title(self, title: str) -> bool:
        """بررسی وجود مقاله با عنوان مشخص"""
        pass
    
    @abstractmethod
    def get_all_published(self, page: int = 1, page_size: int = 10) -> List[Article]:
        """دریافت لیست مقالات منتشر شده با صفحه‌بندی"""
        pass
    
    @abstractmethod
    def get_by_author(self, author_id: str, status: ArticleStatus = None) -> List[Article]:
        """دریافت مقالات یک نویسنده"""
        pass
    
    @abstractmethod
    def get_by_category(self, category_id: str, page: int = 1, page_size: int = 10) -> List[Article]:
        """دریافت مقالات یک دسته‌بندی"""
        pass
    
    @abstractmethod
    def get_by_tag(self, tag_id: str, page: int = 1, page_size: int = 10) -> List[Article]:
        """دریافت مقالات یک تگ"""
        pass
    
    @abstractmethod
    def increment_view_count(self, article_id: str) -> None:
        """افزایش تعداد بازدیدهای مقاله"""
        pass
    
    @abstractmethod
    def get_recent_articles(self, limit: int = 5) -> List[Article]:
        """دریافت آخرین مقالات منتشر شده"""
        pass
    
    @abstractmethod
    def get_popular_articles(self, limit: int = 5) -> List[Article]:
        """دریافت پر بازدیدترین مقالات"""
        pass