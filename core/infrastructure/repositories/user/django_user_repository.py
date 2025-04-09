from django.core.exceptions import ObjectDoesNotExist
from core.domain.exceptions import UserNotFoundError
from .user_model import UserModel
from core.domain.entities.user import User as UserEntity


class DjangoUserRepository:
    """Django implementation of UserRepository"""
    
    def get(self, user_id) -> 'UserEntity':
        try:
            return UserModel.objects.get_by_id(user_id).to_domain()
        except ObjectDoesNotExist:
            raise UserNotFoundError.by_id(user_id.value)

    def get_by_email(self, email) -> 'UserEntity':
        try:
            return UserModel.objects.get_by_email(email).to_domain()
        except ObjectDoesNotExist:
            raise UserNotFoundError.by_email(email.address)

    def save(self, user: 'UserEntity'):
        if hasattr(user, '_orm_model'):
            user._orm_model.update_from_domain(user)
            user._orm_model.save()
        else:
            orm_model = UserModel.from_domain(user)
            orm_model.save()
            user._orm_model = orm_model

    def delete(self, user_id):
        UserModel.objects.filter(id=user_id.value).delete()