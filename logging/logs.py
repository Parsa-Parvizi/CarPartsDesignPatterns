import logging


class BaseLogManager:
    """Base class for managing logs"""

    def __init__(self, filename):
        self.filename = filename
        self.setup_logging()

    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            filename=self.filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def get_logs(self):
        """Retrieve the log contents."""
        try:
            with open(self.filename, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            return []  # Return empty if the file does not exist
        except Exception as e:
            logging.error(f"Error retrieving logs: {e}")
            return []

    def clear_logs(self):
        """Clear all logs."""
        try:
            open(self.filename, 'w').close()  # Clear the log file
        except Exception as e:
            logging.error(f"Error clearing logs: {e}")


class LogManager(BaseLogManager):
    def __init__(self):
        super().__init__('car_parts.log')
        self.setup_logging()

    def log_action(self, action):
        """Log an action with error handling"""
        try:
            if "logged in" not in action and "logged out" not in action:
                logging.info(action)
        except Exception as e:
            print(f"Error logging action: {e}")

    def log_login(self, username):
        """Log user login."""
        logging.info(f"User '{username}' logged in.")

    def log_logout(self, username):
        """Log user logout."""
        logging.info(f"User '{username}' logged out.")

    def get_login_logout_logs(self):
        """Retrieve only login and logout logs."""
        all_logs = self.get_logs()
        return [log for log in all_logs if "logged in" in log or "logged out" in log]


class PartLogManager(BaseLogManager):
    def __init__(self):
        super().__init__('part_activity.log')

    def log_action(self, action):
        """Log an action performed in the application related to parts."""
        logging.info(action)


class UserLogManager(BaseLogManager):
    def __init__(self):
        super().__init__('user_activity.log')

    def log_login(self, username):
        """Log user login."""
        logging.info(f"User '{username}' logged in.")

    def log_logout(self, username):
        """Log user logout."""
        logging.info(f"User '{username}' logged out.")

    def get_login_logout_logs(self):
        """Retrieve only login and logout logs."""
        all_logs = self.get_logs()
        return [log for log in all_logs if "logged in" in log or "logged out" in log]
