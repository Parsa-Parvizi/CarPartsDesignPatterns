import unittest
from unittest.mock import MagicMock, patch
from car_parts import CarPartDatabase
from car_parts_app import CarPartsApp


class TestCarPartsAppIntegration(unittest.TestCase):

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

    def test_add_part_integration(self):
        # Setup mock return values
        self.mock_database.add_part = MagicMock()

        # Simulate adding a part
        self.app.part_type_entry = MagicMock(return_value='Engine')
        self.app.part_name_entry = MagicMock(return_value='V8')
        self.app.price_entry = MagicMock(return_value='5000')

        self.app.add_part()

        # Check if the add_part method was called with the correct parameters
        self.mock_database.add_part.assert_called_with('Engine', 'V8', 5000)

    def test_get_price_integration(self):
        # Setup mock return value
        self.mock_database.get_price.return_value = 5000

        # Simulate retrieving a part price
        self.app.retrieve_part_entry = MagicMock(return_value='V8')
        price = self.app.get_price()

        # Check if the price is retrieved correctly
        self.assertEqual(price, 5000)
        self.mock_database.get_price.assert_called_with('Engine', 'V8')

    def test_edit_part_integration(self):
        # Setup mock return values
        self.mock_database.edit_part = MagicMock(return_value=True)

        # Simulate editing a part price
        with patch('tkinter.simpledialog.askstring', return_value='V8'):
            with patch('tkinter.simpledialog.askfloat', return_value=6000):
                self.app.edit_part()

        # Check if the edit_part method was called with the correct parameters
        self.mock_database.edit_part.assert_called_with('V8', 6000)

    def test_delete_part_integration(self):
        # Setup mock return values
        self.mock_database.delete_part = MagicMock(return_value=True)

        # Simulate deleting a part
        with patch('tkinter.simpledialog.askstring', return_value='V8'):
            self.app.delete_part()

        # Check if the delete_part method was called with the correct parameters
        self.mock_database.delete_part.assert_called_with('V8')

    def test_login_integration(self):
        # Setup mock return values
        self.mock_auth.login.return_value = "123456"  # Mock a 2FA token

        # Simulate user login
        self.app.username_entry = MagicMock(return_value='test_user')
        self.app.password_entry = MagicMock(return_value='password')

        with patch('tkinter.simpledialog.askstring', return_value='123456'):
            self.app.login()

        # Check if the login method was called correctly
        self.mock_auth.login.assert_called_with('test_user', 'password')

    def test_logout_integration(self):
        # Simulate user logout
        self.app.current_user = 'test_user'
        self.app.logout()

        # Check if the logout method was called correctly
        self.mock_log_manager.log_logout.assert_called_with('test_user')


if __name__ == '__main__':
    unittest.main()
