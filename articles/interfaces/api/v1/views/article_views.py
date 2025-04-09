from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from application.use_cases.article_management.create_article import CreateArticleUseCase
from application.use_cases.article_management.update_article import UpdateArticleUseCase
from application.use_cases.article_management.publish_article import PublishArticleUseCase
from application.use_cases.article_management.archive_article import ArchiveArticleUseCase
from interfaces.api.v1.serializers.article_serializer import ArticleSerializer
from domain.exceptions.article_errors import ArticleNotFoundError
from infrastructure.repositories.article.django_article_repository import DjangoArticleRepository
from infrastructure.services.search.elasticsearch_adapter import ElasticsearchAdapter

class ArticleAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ArticleSerializer

    def __init__(self):
        self.article_repo = DjangoArticleRepository()
        self.search_service = ElasticsearchAdapter()
        super().__init__()

    def get(self, request, article_id=None):
        """دریافت مقاله/مقالات"""
        if article_id:
            # دریافت مقاله خاص
            article = self.article_repo.get_by_id(article_id)
            if not article:
                return Response(
                    {'error': 'مقاله یافت نشد'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = self.serializer_class(article)
            return Response(serializer.data)
        
        # دریافت لیست مقالات
        articles = self.article_repo.get_all_published()
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ایجاد مقاله جدید"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        use_case = CreateArticleUseCase(
            article_repository=self.article_repo,
            search_service=self.search_service
        )
        
        try:
            article = use_case.execute({
                'title': serializer.validated_data['title'],
                'content': serializer.validated_data['content'],
                'author': request.user,
                'tags': serializer.validated_data.get('tags', []),
                'categories': serializer.validated_data.get('categories', []),
                'status': serializer.validated_data['status']
            })
            return Response(
                self.serializer_class(article).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    # سایر متدها (PUT, DELETE, etc.)