from django.db import transaction
from typing import List, Optional
from domain.models.comment import Comment
from domain.value_objects.comment_status import CommentStatus
from application.interfaces.repositories.comment_repository import CommentRepository
from ...repositories.comment.django_comment_repository import DjangoComment

class DjangoCommentRepository(CommentRepository):
    """پیاده‌سازی ریپازیتوری کامنت با استفاده از Django ORM"""
    
    def get_by_id(self, comment_id: str) -> Optional[Comment]:
        try:
            db_comment = DjangoComment.objects.get(id=comment_id)
            return self._to_domain(db_comment)
        except DjangoComment.DoesNotExist:
            return None

    @transaction.atomic
    def save(self, comment: Comment) -> Comment:
        db_comment, created = DjangoComment.objects.update_or_create(
            id=comment.id,
            defaults={
                'content': comment.content,
                'author_id': comment.author.id,
                'article_id': comment.article_id,
                'status': comment.status.value,
                'parent_id': comment.parent_id
            }
        )
        return self._to_domain(db_comment)

    def _to_domain(self, db_comment: DjangoComment) -> Comment:
        from core.domain.models.user import User
        
        return Comment(
            content=db_comment.content,
            author=User(
                id=db_comment.author.id,
                username=db_comment.author.username
            ),
            article_id=db_comment.article_id,
            parent_id=db_comment.parent_id,
            status=CommentStatus(db_comment.status)
        )

    # سایر متدهای ریپازیتوری...