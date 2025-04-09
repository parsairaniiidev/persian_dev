from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from domain.models.article import Article
from core.domain.models.user import User

@dataclass
class ArticleResponseSchema:
    """اسکیما برای پاسخ API مقالات"""
    article: Article
    related_articles: List[Article]
    comment_count: int
    author_details: dict
    
    @property
    def to_dict(self):
        return {
            'article': self._article_to_dict(self.article),
            'related_articles': [
                self._article_to_dict(a) for a in self.related_articles
            ],
            'comment_count': self.comment_count,
            'author': self.author_details
        }
    
    def _article_to_dict(self, article: Article) -> dict:
        return {
            'id': str(article.id),
            'title': article.title,
            'slug': article.slug.value,
            'content': article.content,
            'status': article.status.value,
            'published_at': article.published_at.isoformat() if article.published_at else None,
            'view_count': article.view_count,
            'tags': article.tags,
            'categories': article.categories
        }

@dataclass
class ArticleListSchema:
    """اسکیما برای لیست مقالات"""
    articles: List[Article]
    total_count: int
    page: int
    page_size: int
    
    def to_dict(self):
        return {
            'articles': [
                {
                    'id': str(a.id),
                    'title': a.title,
                    'slug': a.slug.value,
                    'summary': f"{a.content[:100]}..." if len(a.content) > 100 else a.content,
                    'published_at': a.published_at.isoformat() if a.published_at else None,
                    'view_count': a.view_count
                }
                for a in self.articles
            ],
            'pagination': {
                'total': self.total_count,
                'page': self.page,
                'page_size': self.page_size,
                'total_pages': (self.total_count + self.page_size - 1) // self.page_size
            }
        }