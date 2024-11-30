import pyotp
from tkinter import messagebox, simpledialog


class AuthenticationError(Exception):
    """Base class for authentication-related errors."""
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
        self.user_database = {}  # Consider using a persistent database

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            message = self.auth.register(username, password)
            messagebox.showinfo("Registration Successful", message)
        except UsernameAlreadyExistsError as e:
            messagebox.showerror("Registration Error", str(e))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            token = self.auth.login(username, password)
            messagebox.showinfo("2FA Token", f"Your 2FA token is: {token}")
            entered_token = simpledialog.askstring(
                "2FA Verification", "Enter your 2FA token:")
            if self.auth.verify_token(username, entered_token):
                messagebox.showinfo("Login Successful",
                                    f"Welcome, {username}!")
            else:
                messagebox.showerror("Login Error", "Invalid 2FA token.")
        except InvalidCredentialsError as e:
            messagebox.showerror("Login Error", str(e))
        except TokenVerificationError as e:
            messagebox.showerror("Token Verification Error", str(e))

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
