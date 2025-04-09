# core/interfaces/api/v1/schemas/users.py
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginSchema(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    ip_address = serializers.CharField(required=False)

class TokenResponseSchema(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user_id = serializers.IntegerField()
    expires_in = serializers.IntegerField()

    @classmethod
    def from_user(cls, user, tokens):
        return cls({
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh'],
            'user_id': user.id,
            'expires_in': 3600
        })
    
# core/interfaces/api/schemas/users.py
from rest_framework import serializers
from core.domain.models.user import User

class UserProfileSerializer(serializers.ModelSerializer):
    """
    سریالایزر پروفایل کاربر برای API
    """
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'roles', 'created_at']
        read_only_fields = ['id', 'created_at']