from tkinter import Tk
from gui.car_parts_gui import CarPartsApp
from core import CarPartDatabase, Engine, Color
from security.auth import UserAuthentication
# from logs import LogManager, PartLogManager, UserLogManager


def main():
    """
    Main entry point of the Car Parts Management System.
    Initializes and runs the GUI application.
    """
    root = Tk()
    app = CarPartsApp(root)
    root.minsize(500, 400)
    root.mainloop()


if __name__ == "__main__":
    main() 