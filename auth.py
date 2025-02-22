import pyotp
from tkinter import messagebox, simpledialog


class AuthenticationError(Exception):
    """کلاس پایه برای خطاهای مربوط به احراز هویت"""
    pass


class UsernameAlreadyExistsError(AuthenticationError):
    """Raised when a username already exists."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when the username or password is invalid."""
    pass


class TokenVerificationError(AuthenticationError):
    """Raised when token verification fails."""
    pass


class UserAuthentication:
    def __init__(self):
        self.user_database = {}

    def register_user(self, username, password):
        if username in self.user_database:
            raise UsernameAlreadyExistsError("نام کاربری قبلاً وجود دارد")
        
        secret = pyotp.random_base32()
        self.user_database[username] = (password, secret)
        return "ثبت‌نام با موفقیت انجام شد"

    def login(self, username, password):
        if username not in self.user_database:
            raise InvalidCredentialsError("نام کاربری یا رمز عبور نامعتبر است")
        
        stored_password, secret = self.user_database[username]
        if password != stored_password:
            raise InvalidCredentialsError("نام کاربری یا رمز عبور نامعتبر است")
        
        totp = pyotp.TOTP(secret)
        return totp.now()

    def verify_token(self, username, entered_token):
        """Verify the 2FA token."""
        if username in self.user_database:
            _, secret = self.user_database[username]
            totp = pyotp.TOTP(secret)
            if not totp.verify(entered_token):
                raise TokenVerificationError("Invalid 2FA token.")
            return True
        raise TokenVerificationError("Invalid 2FA token.")

    def logout(self, username):
        """Handle user logout."""
        if username in self.user_database:
            return f"User  '{username}' logged out successfully."
        return "No user is logged in."

    def register(self, username, password):
        """ثبت‌نام کاربر جدید"""
        if username in self.user_database:
            raise UsernameAlreadyExistsError("نام کاربری قبلاً وجود دارد")
        
        # ایجاد کلید رمز دو مرحله‌ای
        secret = pyotp.random_base32()
        self.user_database[username] = (password, secret)
        return "ثبت‌نام با موفقیت انجام شد"
