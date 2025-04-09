from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from core.domain.entities.user import User as UserEntity
from core.domain.value_objects.email import Email, UserId

class UserModelManager(models.Manager):
    def get_by_email(self, email: Email) -> 'UserModel':
        return self.get(email=email.address)
    
    def get_by_id(self, user_id: UserId) -> 'UserModel':
        return self.get(id=user_id.value)

class UserModel(AbstractBaseUser, PermissionsMixin):
    """Django ORM model for User persistence"""
    
    id = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # 2FA fields
    two_factor_enabled = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=32, blank=True)
    backup_codes = models.JSONField(default=list)
    
    objects = UserModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def to_domain(self) -> UserEntity:
        """Converts ORM model to domain entity"""
        return UserEntity(
            id=UserId(str(self.id)),
            email=Email(self.email),
            first_name=self.first_name,
            last_name=self.last_name,
            is_active=self.is_active,
            is_verified=self.is_verified,
            two_factor_enabled=self.two_factor_enabled,
            metadata={
                'date_joined': self.date_joined,
                'last_login': self.last_login
            }
        )

    @classmethod
    def from_domain(cls, entity: UserEntity) -> 'UserModel':
        """Creates ORM model from domain entity"""
        return cls(
            id=entity.id.value,
            email=entity.email.address,
            first_name=entity.first_name,
            last_name=entity.last_name,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            two_factor_enabled=entity.two_factor_enabled,
            date_joined=entity.metadata.get('date_joined', timezone.now())
        )

    def update_from_domain(self, entity: UserEntity):
        """Updates existing model from domain entity"""
        self.email = entity.email.address
        self.first_name = entity.first_name
        self.last_name = entity.last_name
        self.is_active = entity.is_active
        self.is_verified = entity.is_verified
        self.two_factor_enabled = entity.two_factor_enabled