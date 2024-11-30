import unittest
from unittest.mock import MagicMock, patch
from car_parts_app import CarPartsApp


class TestCarPartsAppSmoke(unittest.TestCase):

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

    def test_application_initialization(self):
        """Test if the application initializes without errors."""
        self.assertIsNotNone(self.app)

    def test_login_button_enabled(self):
        """Test if the login button is enabled initially."""
        self.assertTrue(self.app.login_button['state'], 'normal')

    def test_logout_button_disabled(self):
        """Test if the logout button is disabled initially."""
        self.assertTrue(self.app.logout_button['state'], 'disabled')

    def test_add_part_functionality(self):
        """Test if adding a part works without errors."""
        self.app.part_type_entry = MagicMock(return_value='Engine')
        self.app.part_name_entry = MagicMock(return_value='V8')
        self.app.price_entry = MagicMock(return_value='5000')

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.add_part()
            mock_showinfo.assert_called_with(
                "Success", "Part 'V8' added successfully!")

    def test_get_price_functionality(self):
        """Test if getting the price of a part works without errors."""
        self.mock_database.get_price.return_value = 5000
        self.app.retrieve_part_entry = MagicMock(return_value='V8')

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.get_price()
            mock_showinfo.assert_called_with(
                "Price", "The price of 'V8' is 5000.")


if __name__ == '__main__':
    unittest.main()
