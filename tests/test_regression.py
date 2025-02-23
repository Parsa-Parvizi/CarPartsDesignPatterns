import unittest
from unittest.mock import MagicMock, patch
from car_parts_app import CarPartsApp


class TestCarPartsAppRegression(unittest.TestCase):

    @patch('car_parts_app.CarPartDatabase')
    @patch('car_parts_app.UserAuthentication')
    @patch('car_parts_app.LogManager')
    def setUp(self, MockLogManager, MockUserAuthentication, MockCarPartDatabase):
        self.mock_database = MockCarPartDatabase.return_value
        self.mock_auth = MockUserAuthentication.return_value
        self.mock_log_manager = MockLogManager.return_value

        # Create an instance of the CarPartsApp with a MagicMock root
        self.app = CarPartsApp(MagicMock())
        self.app.database = self.mock_database
        self.app.auth = self.mock_auth
        self.app.log_manager = self.mock_log_manager

    def test_add_part_regression(self):
        """Test adding a part to ensure it works after changes."""
        self.app.part_type_entry = MagicMock()
        self.app.part_name_entry = MagicMock()
        self.app.price_entry = MagicMock()

        self.app.part_type_entry.get.return_value = 'Tire'
        self.app.part_name_entry.get.return_value = 'All-Season Tire'
        self.app.price_entry.get.return_value = '150'

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.add_part()
            self.mock_database.add_part.assert_called_with(
                'Tire', 'All-Season Tire', 150)
            mock_showinfo.assert_called_with(
                "Success", "Part 'All-Season Tire' added successfully!")

    def test_get_price_regression(self):
        """Test getting the price of a part to ensure it works after changes."""
        self.mock_database.get_price.return_value = 150
        self.app.retrieve_part_entry = MagicMock(
            return_value='All-Season Tire')

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.get_price()
            mock_showinfo.assert_called_with(
                "Price", "The price of 'All-Season Tire' is 150.")

    def test_edit_part_regression(self):
        """Test editing a part's price to ensure it works after changes."""
        self.mock_database.edit_part.return_value = True
        self.app.part_name_entry = MagicMock(return_value='All-Season Tire')

        with patch('tkinter.simpledialog.askfloat', return_value=200):
            with patch('tkinter.messagebox.showinfo') as mock_showinfo:
                self.app.edit_part()
                self.mock_database.edit_part.assert_called_with(
                    'All-Season Tire', 200)
                mock_showinfo.assert_called_with(
                    "Success", "Part 'All-Season Tire' updated successfully!")

    def test_delete_part_regression(self):
        """Test deleting a part to ensure it works after changes."""
        self.mock_database.delete_part.return_value = True
        self.app.part_name_entry = MagicMock(return_value='All-Season Tire')

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.delete_part()
            self.mock_database.delete_part.assert_called_with(
                'All-Season Tire')
            mock_showinfo.assert_called_with(
                "Success", "Part 'All-Season Tire' deleted successfully!")

    def test_user_login_regression(self):
        """Test user login to ensure it works after changes."""
        self.mock_auth.login.return_value = "123456"  # Mock a 2FA token
        self.app.username_entry = MagicMock(return_value='test_user')
        self.app.password_entry = MagicMock(return_value='password')

        with patch('tkinter.simpledialog.askstring', return_value='123456'):
            with patch('tkinter.messagebox.showinfo') as mock_showinfo:
                self.app.login()
                self.mock_auth.login.assert_called_with(
                    'test_user', 'password')
                mock_showinfo.assert_called_with(
                    "Login Successful", "Welcome, test_user!")

    def test_user_logout_regression(self):
        """Test user logout to ensure it works after changes."""
        self.app.current_user = 'test_user'

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.logout()
            self.mock_log_manager.log_logout.assert_called_with('test_user')
            mock_showinfo.assert_called_with(
                "Logout Successful", "You have been logged out.")


if __name__ == '__main__':
    unittest.main()
