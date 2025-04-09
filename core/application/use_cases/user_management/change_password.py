# core/application/use_cases/user_management/change_password.py
import re
from core.domain.exceptions import PasswordComplexityError
from core.domain.exceptions import InvalidCredentialsError

class ChangePasswordUseCase:
    """
    سرویس تغییر رمز عبور کاربر
    """
    def __init__(self, user_repository, password_hasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, user_id: int, old_password: str, new_password: str):
        # بررسی پیچیدگی رمز عبور
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$", new_password):
            raise PasswordComplexityError()
        
        user = self.user_repository.find_by_id(user_id)
        
        # بررسی تطابق رمز قدیمی
        if not self.password_hasher.verify_password(old_password, user.password_hash):
            raise InvalidCredentialsError("رمز عبور فعلی نادرست است")
        
        # به روزرسانی رمز جدید
        user.password_hash = self.password_hasher.hash_password(new_password)
        self.user_repository.update(user)