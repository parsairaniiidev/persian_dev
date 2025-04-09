# core/infrastructure/security/advanced_password_hasher.py
import bcrypt
from core.domain.exceptions import PasswordHashingError

class AdvancedPasswordHasher:
    def hash_password(self, password: str) -> str:
        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            raise PasswordHashingError(f"خطا در هش کردن رمز عبور: {str(e)}")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            raise PasswordHashingError(f"خطا در تأیید رمز عبور: {str(e)}")