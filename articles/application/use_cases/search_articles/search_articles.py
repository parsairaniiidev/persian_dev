from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from domain.models.article import Article
from application.interfaces.services.search_service import SearchService
from application.interfaces.services.statistics_service import StatisticsService

@dataclass
class SearchArticlesDTO:
    """شیء انتقال داده برای جستجوی مقالات"""
    query: str
    page: int = 1
    page_size: int = 10
    filters: Optional[dict] = None
    sort_by: Optional[str] = None

@dataclass
class SearchResult:
    """نتیجه جستجو"""
    articles: List[Article]
    total_results: int
    page: int
    page_size: int

class SearchArticlesUseCase:
    """یوزکیس جستجوی پیشرفته مقالات"""
    
    def __init__(
        self,
        search_service: SearchService,
        statistics_service: StatisticsService
    ):
        self.search_service = search_service
        self.statistics_service = statistics_service

    def execute(self, dto: SearchArticlesDTO) -> SearchResult:
        """
        جستجوی مقالات با قابلیت فیلتر و مرتب‌سازی
        
        Args:
            dto: داده‌های مورد نیاز برای جستجو
            
        Returns:
            SearchResult: نتیجه جستجو شامل لیست مقالات و اطلاعات صفحه‌بندی
        """
        # اعتبارسنجی داده‌های ورودی
        self._validate_input(dto)
        
        # انجام جستجو
        search_results = self.search_service.search_articles(
            query=dto.query,
            page=dto.page,
            page_size=dto.page_size,
            filters=dto.filters,
            sort_by=dto.sort_by
        )
        
        # ثبت آمار جستجو
        self.statistics_service.record_search(
            query=dto.query,
            result_count=search_results.total_results
        )
        
        return SearchResult(
            articles=search_results.articles,
            total_results=search_results.total_results,
            page=dto.page,
            page_size=dto.page_size
        )

    def _validate_input(self, dto: SearchArticlesDTO) -> None:
        """اعتبارسنجی داده‌های ورودی"""
        if not dto.query or len(dto.query.strip()) < 3:
            raise ValueError("عبارت جستجو باید حداقل ۳ کاراکتر داشته باشد")
            
        if dto.page < 1:
            raise ValueError("شماره صفحه نمی‌تواند کمتر از ۱ باشد")
            
        if dto.page_size < 1 or dto.page_size > 100:
            raise ValueError("تعداد نتایج در هر صفحه باید بین ۱ تا ۱۰۰ باشد")