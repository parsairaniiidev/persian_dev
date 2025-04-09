# domain/repositories/article_stats_repository.py
from abc import ABC, abstractmethod
from ...domain.entities.article_stats import ArticleStats

class ArticleStatsRepository(ABC):
    @abstractmethod
    def save(self, stats: ArticleStats) -> None:
        pass

    @abstractmethod
    def get_by_article(self, article_id: str) -> ArticleStats:
        pass