from datetime import datetime
from articles.domain.models.comment import Comment 
from uuid import uuid4
from dataclasses import dataclass
from typing import List
from articles.domain.models.category import Category
from articles.domain.models.tag import Tag
from core.domain.models.user import User
from domain.value_objects.article_status import ArticleStatus
from domain.value_objects.slug import Slug

@dataclass
class Article:
    """
    موجودیت مقاله با تمام قوانین کسب و کار
    شامل اعتبارسنجی‌ها و رفتارهای مربوط به مقاله
    """
    id: str
    title: str
    slug: Slug
    content: str
    author: User
    status: ArticleStatus
    tags: List['Tag']
    categories: List['Category']
    comments: List['Comment']
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None
    view_count: int

    def __init__(
        self,
        title: str,
        content: str,
        author: User,
        tags: List['Tag'] = None,
        categories: List['Category'] = None,
        status: ArticleStatus = ArticleStatus.DRAFT
    ):
        self.id = str(uuid4())
        self.title = title
        self.slug = Slug.generate_from_title(title)
        self.content = content
        self.author = author
        self.status = status
        self.tags = tags or []
        self.categories = categories or []
        self.comments = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.published_at = None
        self.view_count = 0

    def publish(self) -> None:
        """انتشار مقاله با اعتبارسنجی وضعیت فعلی"""
        if self.status == ArticleStatus.PUBLISHED:
            raise ValueError("مقاله قبلا منتشر شده است")
        if not self.content:
            raise ValueError("محتوای مقاله نمی‌تواند خالی باشد")

        self.status = ArticleStatus.PUBLISHED
        self.published_at = datetime.now()
        self.updated_at = datetime.now()

    def add_comment(self, comment: 'Comment') -> None:
        """افزودن کامنت به مقاله با اعتبارسنجی"""
        if self.status != ArticleStatus.PUBLISHED:
            raise ValueError("فقط مقالات منتشر شده می‌توانند کامنت دریافت کنند")
        self.comments.append(comment)
        self.updated_at = datetime.now()

    def increment_view_count(self) -> None:
        """افزایش تعداد بازدیدهای مقاله"""
        self.view_count += 1
        self.updated_at = datetime.now()