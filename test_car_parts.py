import unittest
from car_parts import CarPartDatabase, Engine


class TestCarPartDatabase(unittest.TestCase):

    def setUp(self):
        self.database = CarPartDatabase()
        self.database.add_part("Engine", "V8", 1000)
        self.database.add_part("Color", "Red", 500)

    def test_get_part_existing(self):
        price = self.database.get_price("Engine", "V8")
        self.assertEqual(price, 1000)

    def test_get_part_non_existing(self):
        price = self.database.get_price("Engine", "V6")
        self.assertIsNone(price)

    def test_add_part(self):
        self.database.add_part("Tire", "Michelin", 150)
        price = self.database.get_price("Tire", "Michelin")
        self.assertEqual(price, 150)

    def test_remove_part(self):
        self.database.remove_part("Engine", "V8")
        price = self.database.get_price("Engine", "V8")
        self.assertIsNone(price)


class TestEngine(unittest.TestCase):

    def test_engine_initialization(self):
        engine = Engine("V6")
        self.assertEqual(engine.get_name(), "Engine V6")
        self.assertEqual(engine.get_price(), 300)  # Assuming V6 price is 300

    def test_invalid_engine_power(self):
        with self.assertRaises(ValueError):
            Engine("V10")  # Invalid power


# Scripts: python -m unittest test_car_parts.py

if __name__ == '__main__':
    unittest.main()
