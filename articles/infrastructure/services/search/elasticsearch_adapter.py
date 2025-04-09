from elasticsearch import Elasticsearch
from typing import List, Optional
from dataclasses import dataclass
from domain.models.article import Article
from application.interfaces.services.search_service import SearchService
from config import settings

@dataclass
class ESSearchResult:
    articles: List[Article]
    total_results: int

class ElasticsearchAdapter(SearchService):
    """پیاده‌سازی سرویس جستجو با Elasticsearch"""
    
    def __init__(self):
        self.client = Elasticsearch(
            hosts=[settings.ELASTICSEARCH_URL],
            http_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
        )
        self.index_name = "articles"

    def search_articles(
        self,
        query: str,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[dict] = None,
        sort_by: Optional[str] = None
    ) -> ESSearchResult:
        # ساخت کوئری جستجو
        search_query = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^3", "content"]
                        }
                    },
                    "filter": self._build_filters(filters)
                }
            },
            "from": (page - 1) * page_size,
            "size": page_size,
            "highlight": {
                "fields": {
                    "content": {}
                }
            }
        }

        # اضافه کردن مرتب‌سازی
        if sort_by:
            search_query["sort"] = self._get_sort(sort_by)

        # اجرای جستجو
        response = self.client.search(
            index=self.index_name,
            body=search_query
        )

        # تبدیل نتایج
        articles = [
            self._hit_to_article(hit)
            for hit in response['hits']['hits']
        ]

        return ESSearchResult(
            articles=articles,
            total_results=response['hits']['total']['value']
        )

    def _build_filters(self, filters: Optional[dict]) -> List[dict]:
        """ساخت فیلترهای جستجو"""
        if not filters:
            return []
        
        filter_list = []
        if 'status' in filters:
            filter_list.append({"term": {"status": filters['status']}})
        if 'author_id' in filters:
            filter_list.append({"term": {"author_id": filters['author_id']}})
        if 'tags' in filters:
            filter_list.append({"terms": {"tags": filters['tags']}})
        
        return filter_list

    def _get_sort(self, sort_by: str) -> List[dict]:
        """تبدیل پارامتر مرتب‌سازی به فرمت Elasticsearch"""
        sort_mapping = {
            'newest': {'published_at': 'desc'},
            'oldest': {'published_at': 'asc'},
            'popular': {'view_count': 'desc'},
            'most_commented': {'comment_count': 'desc'}
        }
        return [sort_mapping.get(sort_by, {'published_at': 'desc'})]

    def _hit_to_article(self, hit: dict) -> Article:
        """تبدیل نتیجه جستجو به مدل مقاله"""
        source = hit['_source']
        highlight = hit.get('highlight', {})
        
        from domain.models.article import Article
        from core.domain.models.user import User
        
        return Article(
            id=hit['_id'],
            title=source['title'],
            content=highlight.get('content', [source['content']])[0],
            author=User(id=source['author_id']),
            status=source['status'],
            view_count=source.get('view_count', 0),
            published_at=source.get('published_at')
        )

    # سایر متدهای SearchService...