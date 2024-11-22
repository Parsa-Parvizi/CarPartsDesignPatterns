import sqlite3


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


if __name__ == "__main__":
    conn = create_connection('car_parts.db')
    create_tables(conn)
    insert_car_part(conn, 'Brake Pad', 'Brake System')
    insert_engine(conn, 'V8', 450)
    print(get_car_parts(conn))
    print(get_engines(conn))
    close_connection(conn)
