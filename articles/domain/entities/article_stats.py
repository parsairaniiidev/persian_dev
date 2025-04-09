# domain/entities/article_stats.py
from dataclasses import dataclass

@dataclass
class ArticleStats:
    article_id: str
    view_count: int = 0
    share_count: int = 0
    average_read_time: float = 0.0