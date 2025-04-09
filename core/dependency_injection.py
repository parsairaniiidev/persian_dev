# core/dependency_injection.py
from dependency_injector import containers, providers
from core.application.interfaces.services.auth_service import AuthenticationService
from core.infrastructure.repositories.user.django_user_repository import DjangoUserRepository
from core.infrastructure.security.password_hasher import AdvancedPasswordHasher
from core.infrastructure.security.jwt_provider import JWTProvider
class CoreContainer(containers.DeclarativeContainer):
    user_repository = providers.Singleton(DjangoUserRepository)
    
    password_hasher = providers.Singleton(AdvancedPasswordHasher)
    
    jwt_provider = providers.Singleton(
        JWTProvider,
        secret_key=providers.config.jwt.secret_key,
        algorithm=providers.config.jwt.algorithm
    )
    
    auth_service = providers.Factory(
        AuthenticationService,
        user_repository=user_repository,
        password_hasher=password_hasher,
        jwt_provider=jwt_provider
    )