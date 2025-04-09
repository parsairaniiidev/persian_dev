from rest_framework import serializers
from domain.models.article import Article
from core.domain.models.user import User
from interfaces.api.schemas.articles import ArticleResponseSchema

class ArticleSerializer(serializers.Serializer):
    """سریالایزر برای مقالات (ورودی و خروجی)"""
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    status = serializers.ChoiceField(choices=[
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
        ('archived', 'بایگانی')
    ], default='draft')
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )
    categories = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )

    def create(self, validated_data):
        # این متد در ویوها با استفاده از یوزکیس پیاده‌سازی می‌شود
        pass

    def update(self, instance, validated_data):
        # این متد در ویوها با استفاده از یوزکیس پیاده‌سازی می‌شود
        pass

    def to_representation(self, instance):
        """تبدیل به فرمت خروجی"""
        if isinstance(instance, ArticleResponseSchema):
            return super().to_representation(instance.article)
        
        return super().to_representation(instance)

class ArticleListSerializer(serializers.ModelSerializer):
    """سریالایزر مختصر برای لیست مقالات"""
    author = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'author', 'summary', 'published_at', 'view_count']
    
    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'full_name': getattr(obj.author, 'full_name', '')
        }
    
    def get_summary(self, obj):
        return f"{obj.content[:150]}..." if len(obj.content) > 150 else obj.content