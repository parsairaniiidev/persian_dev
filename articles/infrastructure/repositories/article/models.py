from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class DjangoArticle(models.Model):
    """مدل دیتابیس برای مقالات"""
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'articles'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['author']),
            models.Index(fields=['slug']),
        ]

class DjangoArticleTag(models.Model):
    """مدل دیتابیس برای تگ‌های مقالات"""
    article = models.ForeignKey(DjangoArticle, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'article_tags'
        unique_together = ('article', 'tag_name')

class DjangoArticleCategory(models.Model):
    """مدل دیتابیس برای دسته‌بندی مقالات"""
    article = models.ForeignKey(DjangoArticle, on_delete=models.CASCADE)
    category_id = models.UUIDField()

    class Meta:
        db_table = 'article_categories'
        unique_together = ('article', 'category_id')