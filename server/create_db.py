import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Connect to the SQLite database specified by db_file. """
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite")
        return conn
    except Error as e:
        print("Error while connecting to database:", e)

def create_table(conn, schema):
    """Create a table from the input sql schema"""
    try:
        c = conn.cursor()
        c.execute(schema)
    except Error as e:
        print("Error while creating table:", e)


def main():
    database = 'userdata.db'

    # SQL schemas
    users = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        photo_filename TEXT
    );"""

    projects = """
    CREATE TABLE IF NOT EXISTS Projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        bta REAL NOT NULL,
        prosjektstart INTEGER NOT NULL,
        analyseperiode INTEGER NOT NULL,
        address TEXT NOT NULL,
        created_date TEXT NOT NULL,
        updated_date TEXT NOT NULL,
        active BOOLEAN NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );"""

    products = """
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT NOT NULL,
        bygningsdel TEXT NOT NULL,
        produktgruppe TEXT NOT NULL,
        utskiftingsintervall INTEGER NOT NULL,
        vedlikeholdsutslipp REAL NOT NULL,
        type TEXT NOT NULL,
        uuid TEXT,
        owner TEXT,
        name TEXT,
        regNo TEXT,
        validUntil TEXT,
        classific TEXT,
        FOREIGN KEY (project_id) REFERENCES Projects(project_id)
    );"""

    product_specs = """
    CREATE TABLE IF NOT EXISTS EmissionFactors (
        emission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        A1 REAL, A2 REAL, A3 REAL, A1A2A3 REAL, A4 REAL,
        C1 REAL, C2 REAL, C3 REAL, C4 REAL, D REAL,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    );"""

    try:
        conn = create_connection(database)
        if conn is not None:
            create_table(conn, users)
            create_table(conn, projects)
            create_table(conn, products)
            create_table(conn, product_specs)

            conn.close()

    except Error as e:
        print(f"Error! Cannot create the database connection.: {e}")

if __name__ == '__main__':
    main()
