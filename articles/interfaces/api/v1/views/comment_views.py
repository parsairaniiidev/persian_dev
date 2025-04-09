from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from application.use_cases.comment_management.add_comment import AddCommentUseCase
from application.use_cases.comment_management.moderate_comment import ModerateCommentUseCase
from interfaces.api.v1.serializers.comment_serializer import (
    CommentSerializer,
    CommentModerationSerializer
)
from infrastructure.repositories.comment.django_comment_repository import DjangoCommentRepository
from infrastructure.services.spam_detection import SimpleSpamDetectionService
from infrastructure.services.notification import EmailNotificationService

class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def __init__(self):
        self.comment_repo = DjangoCommentRepository()
        self.spam_service = SimpleSpamDetectionService()
        self.notification_service = EmailNotificationService()
        super().__init__()

    def post(self, request):
        """افزودن نظر جدید"""
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        use_case = AddCommentUseCase(
            article_repository=None,  # در اینجا نیاز نیست
            comment_repository=self.comment_repo,
            spam_detection_service=self.spam_service,
            notification_service=self.notification_service
        )
        
        try:
            comment = use_case.execute({
                'article_id': serializer.validated_data['article_id'],
                'content': serializer.validated_data['content'],
                'author': request.user,
                'parent_comment_id': serializer.validated_data.get('parent_id')
            })
            return Response(
                self.serializer_class(comment, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CommentModerationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, comment_id):
        """مدیریت نظر (تایید/رد/اسپم)"""
        serializer = CommentModerationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        use_case = ModerateCommentUseCase(
            comment_repository=DjangoCommentRepository(),
            notification_service=EmailNotificationService()
        )
        
        try:
            comment = use_case.execute({
                'comment_id': comment_id,
                'action': serializer.validated_data['action'],
                'moderator': request.user
            })
            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )