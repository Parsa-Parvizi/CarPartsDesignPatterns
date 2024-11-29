import bcrypt
import pyotp
from tkinter import messagebox


class UserAuthentication:
    def __init__(self):
        self.user_database = {}

    def register(self, username, password):
        """Handle user registration."""
        if username in self.user_database:
            return "Username already exists."

        # Hash the password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self.user_database[username] = (hashed_password, pyotp.random_base32())
        return "User  registered successfully!"

    def login(self, username, password):
        """Handle user login."""
        if username in self.user_database:
            hashed_password, secret = self.user_database[username]
            # Check hashed password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                # Generate a 2FA token
                totp = pyotp.TOTP(secret)
                token = totp.now()
                return token
            else:
                return "Invalid username or password."
        else:
            return "Invalid username or password."

    def verify_token(self, username, entered_token):
        """Verify the 2FA token."""
        if username in self.user_database:
            _, secret = self.user_database[username]
            totp = pyotp.TOTP(secret)
            return totp.verify(entered_token)
        return False
