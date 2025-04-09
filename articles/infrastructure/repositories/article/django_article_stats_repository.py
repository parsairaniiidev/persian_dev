# infrastructure/repositories/django_article_stats_repository.py
from domain.repositories.article_stats_repository import ArticleStatsRepository
from domain.entities.article_stats import ArticleStats
from models import ArticleStats  # Your Django model

class DjangoArticleStatsRepository(ArticleStatsRepository):
    def save(self, stats: ArticleStats) -> None:
        django_stats, _ = ArticleStats.objects.update_or_create(
            article_id=stats.article_id,
            defaults={
                'view_count': stats.view_count,
                'share_count': stats.share_count,
                'average_read_time': stats.average_read_time
            }
        )
    
    def get_by_article(self, article_id: str) -> ArticleStats:
        try:
            django_stats = ArticleStats.objects.get(article_id=article_id)
            return ArticleStats(
                article_id=django_stats.article_id,
                view_count=django_stats.view_count,
                share_count=django_stats.share_count,
                average_read_time=django_stats.average_read_time
            )
        except ArticleStats.DoesNotExist:
            return ArticleStats(article_id=article_id)