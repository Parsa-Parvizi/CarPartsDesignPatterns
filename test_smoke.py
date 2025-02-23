import unittest
from unittest.mock import MagicMock, patch
from tkinter import Tk
from car_parts_gui import CarPartsApp


class TestCarPartsAppSmoke(unittest.TestCase):

    def setUp(self):
        """Set up test environment"""
        self.root = Tk()
        with patch('tkinter.messagebox.showinfo'):  # Suppress initial login message
            self.app = CarPartsApp(self.root)

    def tearDown(self):
        """Clean up after tests"""
        self.root.destroy()

    def test_application_initialization(self):
        """Test if the application initializes without errors"""
        self.assertIsNotNone(self.app)
        self.assertIsNotNone(self.app.database)
        self.assertIsNotNone(self.app.auth)
        self.assertIsNotNone(self.app.log_manager)

    def test_entry_fields_exist(self):
        """Test if all required entry fields exist"""
        self.assertIsNotNone(self.app.part_type_entry)
        self.assertIsNotNone(self.app.part_name_entry)
        self.assertIsNotNone(self.app.price_entry)
        self.assertIsNotNone(self.app.retrieve_part_entry)
        self.assertIsNotNone(self.app.username_entry)
        self.assertIsNotNone(self.app.password_entry)

    def test_add_part_functionality(self):
        """Test if adding a part works without errors"""
        # Clear any existing text
        self.app.part_type_entry.delete(0, 'end')
        self.app.part_name_entry.delete(0, 'end')
        self.app.price_entry.delete(0, 'end')
        
        # Insert test values
        self.app.part_type_entry.insert(0, "engines")
        self.app.part_name_entry.insert(0, "V8")
        self.app.price_entry.insert(0, "5000")

        with patch('tkinter.messagebox.showinfo') as mock_showinfo, \
             patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.add_part()
            # Check if either success or error message was shown
            self.assertTrue(mock_showinfo.called or mock_showerror.called)

    def test_get_price_functionality(self):
        """Test if getting the price works without errors"""
        # Clear existing text
        self.app.retrieve_part_entry.delete(0, 'end')
        # Insert test value
        self.app.retrieve_part_entry.insert(0, "V8")
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo, \
             patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.get_price()
            # Check if either success or error message was shown
            self.assertTrue(mock_showinfo.called or mock_showerror.called)

    def test_help_functionality(self):
        """Test if help message shows without errors"""
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.show_help()
            mock_showinfo.assert_called_once()

    def test_view_database_window(self):
        """Test if database view window opens without errors"""
        with patch('tkinter.Toplevel') as mock_toplevel:
            self.app.view_database()
            mock_toplevel.assert_called_once()


if __name__ == '__main__':
    unittest.main()
