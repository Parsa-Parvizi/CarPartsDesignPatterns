import sqlite3
import json
from datetime import datetime
from utils.singleton import SingletonMeta


def create_connection(db_file):
    """
    The function `create_connection` creates a connection to a SQLite database file.

    :param db_file: The `db_file` parameter in the `create_connection` function is a string that
    represents the path to the SQLite database file that you want to connect to
    :return: The function `create_connection` is returning a connection object to a SQLite database
    specified by the `db_file` parameter.
    """
    conn = sqlite3.connect(db_file)
    return conn


def create_tables(conn):
    """
    The function `create_tables` creates two tables, `car_parts` and `engines`, in a given database
    connection if they do not already exist.

    :param conn: The `conn` parameter in the `create_tables` function is a connection object that
    represents a connection to a database. This connection object is used to create a cursor object,
    execute SQL queries to create tables, and commit the changes to the database
    """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_parts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engines (
            id INTEGER PRIMARY KEY,
            model TEXT NOT NULL,
            horsepower INTEGER NOT NULL
        )
    ''')
    conn.commit()


def insert_car_part(conn, name, part_type):
    """
    The `insert_car_part` function inserts a car part with the specified name and type into a database
    connection.

    :param conn: The `conn` parameter is typically a connection object that represents a connection to a
    database. It allows you to interact with the database by executing SQL queries and commands. In the
    context of the `insert_car_part` function, the `conn` parameter is used to execute an SQL `INSERT`
    statement
    :param name: The `name` parameter is a string that represents the name of the car part that you want
    to insert into the database
    :param part_type: The `part_type` parameter in the `insert_car_part` function represents the type of
    car part that you want to insert into the database. This could be something like "engine", "tire",
    "brake pad", "headlight", etc. It helps categorize the car parts in
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO car_parts (name, type) VALUES (?, ?)
    ''', (name, part_type))
    conn.commit()


def insert_engine(conn, model, horsepower):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO engines (model, horsepower) VALUES (?, ?)
    ''', (model, horsepower))
    conn.commit()


def get_car_parts(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM car_parts')
    return cursor.fetchall()


def get_engines(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM engines')
    return cursor.fetchall()


def close_connection(conn):
    if conn:
        conn.close()


class ReportManager(metaclass=SingletonMeta):
    def __init__(self, db_file='reports.db'):
        self.reports = []
        self.conn = self.create_connection(db_file)
        self.create_report_table()

    def create_connection(self, db_file):
        """Create a database connection to the SQLite database."""
        conn = sqlite3.connect(db_file)
        return conn

    def create_report_table(self):
        """Create a table for storing reports if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY,
                engine TEXT NOT NULL,
                color TEXT NOT NULL,
                price REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_car_part(self, name, part_type):
        """Insert a car part into the database."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO car_parts (name, type) VALUES (?, ?)
        ''', (name, part_type))
        self.conn.commit()

    def generate_report(self, car):
        """Generate a report for the car."""
        report = {
            "engine": car.engine.get_name(),
            "color": car.color.get_name(),
            "price": car.engine.get_price() + car.color.get_price(),
            "created_at": datetime.now().isoformat()
        }
        self.reports.append(report)
        print("Report generated:", report)
        self.save_report_to_file(report)
        self.save_report_to_db(report)

    def save_report_to_file(self, report):
        """Save the report to a JSON file."""
        with open('reports.json', 'a') as f:
            f.write(json.dumps(report) + '\n')

    def save_report_to_db(self, report):
        """Save the report to the SQLite database."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reports (engine, color, price, created_at) VALUES (?, ?, ?, ?)
        ''', (report['engine'], report['color'], report['price'], report['created_at']))
        self.conn.commit()

    def get_reports(self):
        return self.reports

    def close(self):
        if self.conn:
            self.conn.close()


class CarPartDatabase(metaclass=SingletonMeta):
    def __init__(self, db_file='car_parts.db'):
        self.conn = self.create_connection(db_file)
        self.create_tables()
        self.parts = {
            "engines": {"V8": 500, "V6": 300},
            "colors": {"red": "FF0000", "blue": "0000FF"},
            "tires": {"Pirelli": 100, "Michelin": 150},
            "wheels": {"alloy": 200, "steel": 50},
            "seats": {"leather": 300, "cloth": 100}
        }

    def create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    specs TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    part_id INTEGER,
                    quantity INTEGER DEFAULT 0,
                    min_quantity INTEGER DEFAULT 5,
                    FOREIGN KEY (part_id) REFERENCES parts (id)
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_part(self, part_type, name, price, specs=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO parts (type, name, price, specs)
                VALUES (?, ?, ?, ?)
            ''', (part_type, name, price, json.dumps(specs) if specs else None))
            
            part_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO inventory (part_id, quantity)
                VALUES (?, 0)
            ''', (part_id,))
            
            self.conn.commit()
            return part_id
        except sqlite3.Error as e:
            print(f"Error adding part: {e}")
            return None

    def get_part(self, part_type, part_name):
        try:
            part_price = self.parts.get(part_type, {}).get(part_name)
            if part_price is None:
                raise ValueError(f"Part '{part_name}' of type '{part_type}' not found.")
            return part_price
        except Exception as e:
            print(f"Error retrieving part: {e}")
            return None

    def update_part(self, part_id, price=None, specs=None):
        try:
            cursor = self.conn.cursor()
            updates = []
            params = []
            
            if price is not None:
                updates.append("price = ?")
                params.append(price)
            if specs is not None:
                updates.append("specs = ?")
                params.append(json.dumps(specs))
            
            if updates:
                query = f"UPDATE parts SET {', '.join(updates)} WHERE id = ?"
                params.append(part_id)
                cursor.execute(query, params)
                self.conn.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Error updating part: {e}")
            return False

    def delete_part(self, part_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM parts WHERE name = ?', (part_name,))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting part: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()


class ReportManager:
    def __init__(self):
        self.reports = []

    def generate_report(self, database):
        report = "Car Parts Report:\n"
        report += "\n".join([f"{name}: {info['type']} - ${info['price']}" 
                           for name, info in database.parts.items()])
        return report if database.parts else "No parts available."


if __name__ == "__main__":
    conn = create_connection('car_parts.db')
    create_tables(conn)
    insert_car_part(conn, 'Brake Pad', 'Brake System')
    insert_engine(conn, 'V8', 450)
    print(get_car_parts(conn))
    print(get_engines(conn))
    close_connection(conn)
