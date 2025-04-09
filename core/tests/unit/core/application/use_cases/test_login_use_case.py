# tests/unit/core/application/use_cases/test_login_use_case.py
import pytest
from unittest.mock import Mock
from core.application.use_cases.authentication import LoginUseCase
from core.domain.exceptions import InvalidCredentialsError

@pytest.fixture
def mock_user_repository():
    repo = Mock()
    repo.find_by_email.return_value = Mock(
        password_hash=...,
        failed_login_attempts=0,
        two_factor_enabled=False
    )
    return repo

def test_successful_login(mock_user_repository):
    auth_service = Mock()
    auth_service.verify_password.return_value = True
    
    use_case = LoginUseCase(
        user_repository=mock_user_repository,
        auth_service=auth_service,
        event_publisher=Mock()
    )
    
    result = use_case.execute({
        'email': 'valid@example.com',
        'password': 'correct_password'
    })
    
    assert 'access_token' in result
    assert 'refresh_token' in result