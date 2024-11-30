import unittest
from car_parts import CarPartDatabase, UserAuthentication, LogManager, ReportManager
from car_parts_app import CarPartsApp
from unittest.mock import patch, MagicMock


class TestCarPartDatabase(unittest.TestCase):

    def setUp(self):
        self.database = CarPartDatabase()

    def test_add_part(self):
        self.database.add_part("Engine", "V8", 5000)
        self.assertIn("V8", self.database.parts)
        self.assertEqual(self.database.parts["V8"]["price"], 5000)

    def test_get_price(self):
        self.database.add_part("Engine", "V8", 5000)
        price = self.database.get_price("Engine", "V8")
        self.assertEqual(price, 5000)

    def test_edit_part(self):
        self.database.add_part("Engine", "V8", 5000)
        self.database.edit_part("V8", 6000)
        self.assertEqual(self.database.parts["V8"]["price"], 6000)

    def test_delete_part(self):
        self.database.add_part("Engine", "V8", 5000)
        self.database.delete_part("V8")
        self.assertNotIn("V8", self.database.parts)


class TestUserAuthentication(unittest.TestCase):

    def setUp(self):
        self.auth = UserAuthentication()

    @patch('auth.UserAuthentication.verify_token')
    def test_login_success(self, mock_verify):
        mock_verify.return_value = True
        token = self.auth.login("test_user", "password")
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 6)

    @patch('auth.UserAuthentication.verify_token')
    def test_login_failure(self, mock_verify):
        mock_verify.return_value = False
        token = self.auth.login("test_user", "wrong_password")
        self.assertNotIsInstance(token, str)


class TestLogManager(unittest.TestCase):

    def setUp(self):
        self.log_manager = LogManager()

    def test_log_login(self):
        with patch('logging.info') as mock_log:
            self.log_manager.log_login("test_user")
            mock_log.assert_called_with("User   'test_user' logged in.")

    def test_log_logout(self):
        with patch('logging.info') as mock_log:
            self.log_manager.log_logout("test_user")
            mock_log.assert_called_with("User   'test_user' logged out.")


class TestReportManager(unittest.TestCase):

    def setUp(self):
        self.database = CarPartDatabase()
        self.report_manager = ReportManager()

    def test_generate_report(self):
        self.database.add_part("Engine", "V8", 5000)
        report = self.report_manager.generate_report(self.database)
        self.assertIn("V8: Engine - $5000", report)


class TestCarPartsApp(unittest.TestCase):

    @patch('car_parts_app.CarPartDatabase')
    def setUp(self, MockDatabase):
        self.mock_database = MockDatabase.return_value
        self.app = CarPartsApp(MagicMock())
        self.app.database = self.mock_database

    def test_add_part(self):
        self.app.part_type_entry = MagicMock(return_value="Engine")
        self.app.part_name_entry = MagicMock(return_value="V8")
        self.app.price_entry = MagicMock(return_value="5000")

        self.app.add_part()
        self.mock_database.add_part.assert_called_with("Engine", "V8", 5000)

    def test_get_price(self):
        self.mock_database.get_price.return_value = 5000
        self.app.retrieve_part_entry = MagicMock(return_value="V8")
        price = self.app.get_price()
        self.assertEqual(price, 5000)


if __name__ == '__main__':
    unittest.main()
