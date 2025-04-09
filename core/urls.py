from django.urls import path
from core.interfaces.api.v1.auth import views as auth_views
from core.interfaces.api.v1.users import views as user_views

urlpatterns = [
    # API Authentication
    path('api/v1/auth/login/', auth_views.LoginAPIView.as_view(), name='login'),
    path('api/v1/auth/refresh/', auth_views.RefreshTokenAPIView.as_view(), name='token-refresh'),
    
    # API Users
    path('api/v1/users/profile/', user_views.UserProfileAPIView.as_view(), name='user-profile'),
    path('api/v1/users/change-password/', user_views.ChangePasswordAPIView.as_view(), name='change-password'),
]