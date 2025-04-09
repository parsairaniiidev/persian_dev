# articles/domain/mappers.py
from domain.models.article  import Article, Comment, Category, Tag
from .value_objects.article_status import ArticleStatus
from .value_objects.slug import Slug

class ArticleMapper:
    @staticmethod
    def to_domain(raw_data: dict) -> Article:
        return Article(
            id=raw_data.get('id'),
            title=raw_data['title'],
            content=raw_data['content'],
            status=ArticleStatus(raw_data['status']),
            slug=Slug(raw_data['slug']),
            # سایر فیلدها
        )

    @staticmethod
    def to_persistence(article: Article) -> dict:
        return {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'status': article.status.value,
            'slug': str(article.slug),
            # سایر فیلدها
        }

# مپ‌کننده‌های مشابه برای Comment, Category, Tag