# The line 'from abc import ABC, abstractmethod' is importing the 'ABC' and 'abstractmethod' classes
# from the 'abc' module in Python.
from abc import ABC, abstractmethod
import copy
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.singleton import SingletonMeta


# The above class implements the Singleton design pattern in Python.
class SingletonMeta(type):
    """
    The line '_instances = {}' is initializing an empty dictionary named '_instances'.
    This dictionary is used to store instances of classes created using the Singleton design pattern.
    The purpose of this dictionary is to keep track of instances created for each class and
    ensure that only one instance of a class exists at any given time.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        The function is a metaclass implementation that ensures only one instance of a class is created.

        :param cls: The 'cls' parameter in the code snippet you provided refers to the class itself.
        When a class is called as a function (like 'MyClass()'), the '__call__' method is invoked, and
        'cls' represents the class being called
        :return: The code snippet provided is a metaclass implementation that ensures only one instance
        of a class is created. When the class is called, it checks if an instance of that class already
        exists in the '_instances' dictionary. If not, it creates a new instance and stores it in the
        dictionary. Finally, it returns the instance of the class that was created or already existed.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# این کلاس یک الگوی Singleton را برای مدیریت پایگاه داده قطعات خودرو پیاده‌سازی می‌کند
class CarPartDatabase(metaclass=SingletonMeta):
    def __init__(self):
        # دیکشنری برای ذخیره انواع مختلف قطعات و قیمت‌های آنها
        self.parts = {
            "engines": {"V8": 500, "V6": 300},  # موتورها و قیمت‌های آنها
            "colors": {"red": "FF0000", "blue": "0000FF"},  # رنگ‌ها و کدهای آنها
            "tires": {"Pirelli": 100, "Michelin": 150},  # لاستیک‌ها و قیمت‌های آنها
            "wheels": {"alloy": 200, "steel": 50},  # چرخ‌ها و قیمت‌های آنها
            "seats": {"leather": 300, "cloth": 100}  # صندلی‌ها و قیمت‌های آنها
        }

    def get(self, part_type, part_name):
        """دریافت یک نمونه از قطعه بر اساس نوع و نام"""
        if part_type == "Engine":
            return Engine(part_name)
        elif part_type == "Color":
            return Color(part_name)
        return None

    def get_part(self, part_type, part_name):
        """دریافت قیمت قطعه بر اساس نوع و نام"""
        try:
            part_price = self.parts.get(part_type, {}).get(part_name)
            if part_price is None:
                raise ValueError(f"قطعه '{part_name}' از نوع '{part_type}' یافت نشد.")
            return part_price
        except Exception as e:
            print(f"خطا در دریافت قطعه: {e}")
            return None

    def add_part(self, part_type, part_name, price):
        if part_name in self.parts:
            raise ValueError("Part already exists")
        self.parts[part_name] = {'type': part_type, 'price': price}
        print(f"Part '{part_name}' added with price {price}.")

    def get_price(self, part_type, part_name):
        part = self.parts.get(part_name)
        if part and part['type'] == part_type:
            return part['price']
        return None

    def edit_part(self, part_name, new_price):
        if part_name in self.parts:
            self.parts[part_name]['price'] = new_price
            return True
        return False

    def remove_part(self, part_type, part_name):
        """
        The function removes a specific part from a dictionary of parts based on the part type and name
        provided.

        :param part_type: The 'part_type' parameter in the 'remove_part' method refers to the type or
        category of the part that you want to remove from the object. It is used to specify the group or
        classification to which the part belongs
        :param part_name: The 'part_name' parameter in the 'remove_part' method refers to the name of
        the specific part that you want to remove from the 'parts' dictionary within the object. This
        method takes two parameters: 'part_type' which specifies the type of part (e.g., 'engine', '
        :return: The 'self' object is being returned after removing the specified part from the 'parts'
        dictionary.
        """
        if part_type in self.parts and part_name in self.parts[part_type]:
            del self.parts[part_type][part_name]
        return self

    def copy(self):
        """
        The function 'copy' returns a deep copy of the object it is called on.
        :return: The 'copy' method is returning a deep copy of the object 'self'. This means that a new
        object is created with the same data as the original object, but they are independent of each
        other.
        """
        return copy.deepcopy(self)


# The 'CarPart' class is an abstract base class with abstract methods 'get_price' and 'get_name' for
# representing car parts.
class CarPart(ABC):
    """Abstract base class for all car parts."""
    
    @abstractmethod
    def get_price(self):
        """
        The above function is an abstract method in Python that defines a method signature for getting
        the price of an object.
        """
        pass

    @abstractmethod
    def get_name(self):
        """
        The function 'get_name' is an abstract method that returns the name of the object.
        """
        pass

    @abstractmethod
    def get_specs(self):
        pass


# The 'Engine' class represents a car engine with a specified power and price.
class Engine(CarPart):
    def __init__(self, power):
        from .CarPartDatabase import CarPartDatabase
        self.db = CarPartDatabase()
        self.power = power
        self.price = 1000

    def get_price(self):
        """
        The function 'get_price' returns the price attribute of an object.
        :return: The 'price' attribute of the object.
        """
        return self.price

    def get_name(self):
        """
        The function 'get_name' returns the string "Engine".
        :return: The function 'get_name' is returning the string "Engine".
        """
        return "Engine"

    def get_specs(self):
        return f"Power: {self.power}, Price: {self.price}"


# The 'Color' class represents a car part with a code attribute and methods to get the price and name.
class Color(CarPart):
    def __init__(self, code):
        self.code = code

    def get_price(self):
        return self.price

    def get_name(self):
        return "Color"

    def get_specs(self):
        return f"Code: {self.code}"


# The 'CarFactory' class is an abstract base class with abstract methods 'create_engine' and
# 'create_color'.
class CarFactory(ABC):
    @abstractmethod
    def create_engine(self):
        pass

    @abstractmethod
    def create_color(self):
        pass


# The 'SedanFactory' class creates a sedan car with a V6 engine and red color by utilizing a
# 'CarPartDatabase'.
class SedanFactory(CarFactory):
    def create_engine(self):
        from .CarPartDatabase import CarPartDatabase
        return Engine(CarPartDatabase().get_part("engines", "V6"))

    def create_color(self):
        from .CarPartDatabase import CarPartDatabase
        return Color(CarPartDatabase().get_part("colors", "red"))


# The 'TruckFactory' class extends the 'CarFactory' class and overrides methods to create a specific
# engine and color for trucks.
class TruckFactory(CarFactory):
    def create_engine(self):
        from .CarPartDatabase import CarPartDatabase
        return Engine(CarPartDatabase().get_part("engines", "V8"))

    def create_color(self):
        from .CarPartDatabase import CarPartDatabase
        return Color(CarPartDatabase().get_part("colors", "blue"))


# The 'CarBuilder' class is used to construct a car object by setting its engine using a factory.
class CarBuilder:
    def __init__(self, factory):
        self.factory = factory
        self.car = None

    def reset(self):
        self.car = None

    def set_engine(self):
        """
        The function sets the engine of a car by creating an engine using a factory.
        """
        try:
            self.car.engine = self.factory.create_engine()
        except Exception as e:
            print(f"Error setting engine: {e}")

    def set_color(self):
        try:
            self.car.color = self.factory.create_color()
        except Exception as e:
            print(f"Error setting color: {e}")

    def build(self):
        return self.car


# The 'Car' class in Python defines a blueprint for creating car objects with engine and color
# attributes, and includes a method to clone the object.
class Car:
    def __init__(self):
        self.engine = None
        self.color = None

    def clone(self):
        return copy.deepcopy(self)


# Concrete Car class
# The 'ConcreteCar' class represents a car with engine and color attributes, providing methods to get
# details and clone the object.
class ConcreteCar(Car):
    def __init__(self):
        self.engine = None
        self.color = None

    def get_details(self):
        return f"Car with {self.engine.get_name()} and {self.color.get_name()}"

    def clone(self):
        return copy.deepcopy(self)


class ReportManager(metaclass=SingletonMeta):
    def __init__(self):
        self.reports = []

    def generate_report(self, car):
        report = {
            "engine": car.engine.get_name(),
            "color": car.color.get_name(),
            "price": car.engine.get_price() + car.color.get_price()
        }
        self.reports.append(report)
        print("Report generated:", report)

    def get_reports(self):
        return self.reports


# Client code
def main():
    try:
        # Create a Sedan
        sedan_factory = SedanFactory()
        sedan_builder = CarBuilder(sedan_factory)
        sedan_builder.set_engine()
        sedan_builder.set_color()
        sedan = sedan_builder.build()
        print(sedan.get_details())

        # Generate report for the sedan
        report_manager = ReportManager()
        report_manager.generate_report(sedan)

        # Create a Truck
        truck_factory = TruckFactory()
        truck_builder = CarBuilder(truck_factory)
        truck_builder.set_engine()
        truck_builder.set_color()
        truck = truck_builder.build()
        print(truck.get_details())

        # Generate report for the truck
        report_manager.generate_report(truck)

        # Retrieve all reports
        all_reports = report_manager.get_reports()
        print("All Reports:", all_reports)

    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        report_manager.close()  # Close the database connection


if __name__ == "__main__":
    main()
