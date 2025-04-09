from rest_framework import serializers
from domain.models.comment import Comment
from core.domain.models.user import User

class CommentSerializer(serializers.Serializer):
    """سریالایزر برای نظرات"""
    id = serializers.UUIDField(read_only=True)
    content = serializers.CharField(max_length=1000)
    article_id = serializers.UUIDField()
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)

    def get_author(self, obj):
        if isinstance(obj, Comment):
            user = obj.author
        else:
            # برای حالتی که obj یک dict است (مثلا در ایجاد کامنت جدید)
            user = self.context['request'].user
        
        return {
            'id': user.id,
            'username': user.username,
            'avatar': getattr(user, 'avatar_url', None)
        }

class CommentModerationSerializer(serializers.Serializer):
    """سریالایزر برای مدیریت نظرات"""
    action = serializers.ChoiceField(choices=[
        ('approve', 'تایید'),
        ('reject', 'رد'),
        ('spam', 'اسپم')
    ])
    reason = serializers.CharField(required=False, allow_null=True)