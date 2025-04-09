from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ArticleEvent:
    """رویداد پایه برای مقالات"""
    article_id: str
    timestamp: datetime = datetime.now()

@dataclass
class ArticlePublishedEvent(ArticleEvent):
    """رویداد انتشار مقاله"""
    published_by: str  # شناسه کاربر منتشرکننده

@dataclass
class ArticleUpdatedEvent(ArticleEvent):
    """رویداد به‌روزرسانی مقاله"""
    updated_fields: Optional[list[str]] = None

@dataclass
class ArticleViewedEvent(ArticleEvent):
    """رویداد مشاهده مقاله"""
    viewer_id: Optional[str] = None  # شناسه کاربر مشاهده‌کننده (اگر لاگین کرده باشد)

@dataclass
class ArticleCommentedEvent(ArticleEvent):
    """رویداد ثبت کامنت برای مقاله"""
    comment_id: str
    comment_author_id: str