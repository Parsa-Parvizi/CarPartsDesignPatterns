# The line 'from abc import ABC, abstractmethod' is importing the 'ABC' and 'abstractmethod' classes
# from the 'abc' module in Python.
from abc import ABC, abstractmethod
import copy


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


# The 'CarPartDatabase' class is a singleton class that stores information about car parts and allows
# for adding, removing, and retrieving parts.
class CarPartDatabase(metaclass=SingletonMeta):
    def __init__(self):
        self.parts = {
            "engines": {"V8": 500, "V6": 300},
            "colors": {"red": "FF0000", "blue": "0000FF"},
            "tires": {"Pirelli": 100, "Michelin": 150},
            "wheels": {"alloy": 200, "steel": 50},
            "seats": {"leather": 300, "cloth": 100}
        }

    def get_part(self, part_type, part_name):
        """
        The function 'get_part' retrieves a specific part by type and name from a dictionary of parts.

        :param part_type: The 'part_type' parameter in the 'get_part' method is used to specify the type
        of part that you want to retrieve. It is a key that is used to access a dictionary of parts
        within the 'self' object
        :param part_name: The 'part_name' parameter in the 'get_part' method is used to specify the name
        of the part that you want to retrieve from the parts dictionary
        :return: The 'get_part' method is returning the part with the specified 'part_type' and
        'part_name' from the 'parts' dictionary. If the 'part_type' is not found in the dictionary, it
        will return an empty dictionary. If the 'part_name' is not found within the 'part_type'
        dictionary, it will return 'None'.
        """
        try:
            part_price = self.parts.get(part_type, {}).get(part_name)
            if part_price is None:
                raise ValueError(f"Part '{part_name}' of type '{
                                 part_type}' not found.")
            return part_price
        except Exception as e:
            print(f"Error retrieving part: {e}")
            return None

    def add_part(self, part_type, part_name, price):
        """
        The function 'add_part' adds a part with its type, name, and price to a dictionary of parts.

        :param part_type: The 'part_type' parameter in the 'add_part' method refers to the category or
        type of the part being added. It is used to organize the parts within the 'self.parts'
        dictionary
        :param part_name: The 'part_name' parameter in the 'add_part' method refers to the name of the
        part that you want to add to the 'self.parts' dictionary. This method allows you to add a part
        with its corresponding price under a specific 'part_type'
        :param price: The 'price' parameter in the 'add_part' method represents the cost or price of the
        part being added to the object. It is the amount that needs to be paid for that specific part
        :return: The 'add_part' method is returning the instance of the class itself ('self') after
        adding the specified part information to the 'parts' dictionary.
        """
        if part_type not in self.parts:
            self.parts[part_type] = {}
        self.parts[part_type][part_name] = price
        return self

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


# The 'Engine' class represents a car engine with a specified power and price.
class Engine(CarPart):
    def __init__(self, power):
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


# The 'Color' class represents a car part with a code attribute and methods to get the price and name.
class Color(CarPart):
    def __init__(self, code):
        self.code = code

    def get_price(self):
        return self.price

    def get_name(self):
        return "Color"


# The class 'CarPart' is an abstract base class with abstract methods 'get_price' and 'get_name'.
class CarPart(ABC):
    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_name(self):
        pass


# The 'Engine' class represents a car engine with a specified power and price.
class Engine(CarPart):
    def __init__(self, power):
        if power not in ["V8", "V6"]:
            raise ValueError(f"Invalid engine power: {power}")
        self.power = power
        self.price = CarPartDatabase().get_part("engines", power)

    def get_price(self):
        return self.price

    def get_name(self):
        return f"Engine {self.power}"


# The Color class represents a car part with a code and a fixed price of 500.
class Color(CarPart):
    def __init__(self, code):
        if code not in ["red", "blue", "green"]:
            raise ValueError(f"Invalid color code: {code}")
        self.code = code
        self.price = 500  # Fixed price for simplicity

    def get_price(self):
        return self.price

    def get_name(self):
        return f"Color {self.code}"


# The 'CarPartDatabase' class has a method 'get' that returns an instance of a specific part type
# based on the input part name.
class CarPartDatabase:
    def get(self, part_type, part_name):
        """
        The function 'get' returns an instance of a class based on the 'part_type' provided.

        :param part_type: The 'part_type' parameter is used to specify the type of part that you want to
        retrieve. In the provided 'get' method, it is used to determine whether the part being requested
        is an "Engine" or a "Color"
        :param part_name: The 'part_name' parameter is the name or identifier of the specific part that
        you want to retrieve or create an instance of. It could be the name of an engine model, a color
        name, or any other part depending on the 'part_type' specified
        :return: An instance of the 'Engine' class is being returned if the 'part_type' is "Engine", an
        instance of the 'Color' class is being returned if the 'part_type' is "Color", and 'None' is
        being returned if the 'part_type' is neither "Engine" nor "Color".
        """
        if part_type == "Engine":
            return Engine(part_name)
        elif part_type == "Color":
            return Color(part_name)
        return None


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
        return Engine(CarPartDatabase().get_part("engines", "V6"))

    def create_color(self):
        return Color(CarPartDatabase().get_part("colors", "red"))


# The 'TruckFactory' class extends the 'CarFactory' class and overrides methods to create a specific
# engine and color for trucks.
class TruckFactory(CarFactory):
    def create_engine(self):
        return Engine(CarPartDatabase().get_part("engines", "V8"))

    def create_color(self):
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
