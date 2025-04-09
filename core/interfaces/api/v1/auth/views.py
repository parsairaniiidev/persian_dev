# core/interfaces/api/v1/views/auth_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.application.use_cases.authentication.login import LoginUseCase
from core.domain.exceptions import AccountLockedError, InvalidCredentialsError
from core.infrastructure.events import DjangoEventPublisher
from core.infrastructure.repositories.user.django_user_repository import DjangoUserRepository
from core.infrastructure.security.jwt_provider import JWTProvider
from ...schemas.users import UserLoginSchema, TokenResponseSchema

class AuthAPIView(APIView):
    throttle_scope = 'authentication'

    def post(self, request):
        schema = UserLoginSchema(data=request.data)
        if not schema.is_valid():
            return Response(schema.errors, status=status.HTTP_400_BAD_REQUEST)

        use_case = LoginUseCase(
            user_repository=DjangoUserRepository(),
            auth_service=JWTProvider(),
            event_publisher=DjangoEventPublisher()
        )

        try:
            result = use_case.execute(schema.validated_data)
            return Response(TokenResponseSchema.from_user(result))
        except AccountLockedError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except InvalidCredentialsError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)