import unittest
from car_parts import CarPartDatabase, Engine, Color


class TestCarPartDatabase(unittest.TestCase):

    def setUp(self):
        """Reset the singleton instance before each test."""
        CarPartDatabase._instances = {}  # Reset singleton instance
        self.database = CarPartDatabase()

    def test_get_part_existing(self):
        """Test getting an existing part's price"""
        # Test getting price of existing engine
        price = self.database.get_part("engines", "V8")
        self.assertEqual(price, 500)

        # Test getting price of existing color
        price = self.database.get_part("colors", "red")
        self.assertEqual(price, "FF0000")

    def test_get_part_non_existing(self):
        """Test getting a non-existing part's price"""
        # Test non-existing engine
        price = self.database.get_part("engines", "V10")
        self.assertIsNone(price)

        # Test non-existing category
        price = self.database.get_part("nonexistent", "something")
        self.assertIsNone(price)

    def test_get_engine_instance(self):
        """Test getting an engine instance"""
        engine = self.database.get("Engine", "V6")
        self.assertIsInstance(engine, Engine)
        self.assertEqual(engine.get_name(), "Engine")
        self.assertEqual(engine.power, "V6")

    def test_get_color_instance(self):
        """Test getting a color instance"""
        color = self.database.get("Color", "red")
        self.assertIsInstance(color, Color)
        self.assertEqual(color.get_name(), "Color")
        self.assertEqual(color.code, "red")


class TestEngine(unittest.TestCase):

    def test_engine_initialization(self):
        """Test engine initialization"""
        engine = Engine("V6")
        self.assertEqual(engine.get_name(), "Engine")
        self.assertEqual(engine.get_price(), 1000)
        self.assertEqual(engine.power, "V6")


class TestColor(unittest.TestCase):

    def test_color_initialization(self):
        """Test color initialization"""
        color = Color("red")
        self.assertEqual(color.get_name(), "Color")
        self.assertEqual(color.code, "red")


# Scripts: python -m unittest test_car_parts.py

if __name__ == '__main__':
    unittest.main()
