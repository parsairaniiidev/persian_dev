from django.urls import path
from rest_framework.routers import DefaultRouter
from interfaces.api.v1.views.article_views import ArticleAPIView
from interfaces.api.v1.views.comment_views import CommentAPIView, CommentModerationAPIView

router = DefaultRouter()

# مقالات
router.register(r'articles', ArticleAPIView, basename='article')

# نظرات
router.register(r'comments', CommentAPIView, basename='comment')

# مسیرهای اضافی
extra_urlpatterns = [
    path(
        'comments/<uuid:comment_id>/moderate/',
        CommentModerationAPIView.as_view(),
        name='comment-moderate'
    ),
]

def get_urls():
    return router.urls + extra_urlpatterns