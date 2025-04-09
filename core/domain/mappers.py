# core/domain/mappers.py
from .models.user import User, Role
from .value_objects.email import Email

class UserMapper:
    @staticmethod
    def to_domain(raw_data: dict) -> User:
        return User(
            id=raw_data.get('id'),
            email=Email(raw_data['email']),
            username=raw_data['username'],
            is_active=raw_data.get('is_active', False),
            roles=[RoleMapper.to_domain(r) for r in raw_data.get('roles', [])]
        )

    @staticmethod
    def to_persistence(user: User) -> dict:
        return {
            'id': user.id,
            'email': str(user.email),
            'username': user.username,
            'is_active': user.is_active,
            'roles': [RoleMapper.to_persistence(r) for r in user.roles]
        }

class RoleMapper:
    @staticmethod
    def to_domain(raw_data: dict) -> Role:
        return Role(
            id=raw_data.get('id'),
            name=raw_data['name'],
            permissions=raw_data.get('permissions', [])
        )

    @staticmethod
    def to_persistence(role: Role) -> dict:
        return {
            'id': role.id,
            'name': role.name,
            'permissions': role.permissions
        }