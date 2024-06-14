import psycopg2
from psycopg2 import sql, Error
from colorama import Fore
from dotenv import load_dotenv
import os

# get db credentials from environment variables.
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db_credentials.env')
print(f"Loading environment variables from: {env_path}")
load_dotenv(dotenv_path=env_path)

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

conn_params = {
    "dbname": "postgres",
    "user": db_user,
    "password": db_password,
    "host": db_host,
    "port": db_port
}

def create_database(conn, dbname):
    """Creates the database if it does not exist"""
    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        conn.autocommit = False
        print(Fore.GREEN + f"Creation of database {dbname} SUCCEEDED")
    except Error as e:
        if 'already exists' in str(e):
            print(Fore.YELLOW + f"Database {dbname} already exists")
        else:
            print(Fore.RED + f"Error while creating database: {e}")

def create_table(conn, schema):
    """Creates a database table based on an input schema"""
    try:
        cur = conn.cursor()
        cur.execute(schema)
        conn.commit()
    except Error as e:
        print(Fore.RED + f"Error while creating table: {e}")

def main():
    """Defines table schemas for userdata database and creates the tables"""

    users = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        photo_filename TEXT
    );"""

    projects = """
    CREATE TABLE IF NOT EXISTS projects (
        project_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        bta REAL NOT NULL,
        prosjektstart INTEGER NOT NULL,
        analyseperiode INTEGER NOT NULL,
        address TEXT NOT NULL,
        created_date TEXT NOT NULL,
        updated_date TEXT NOT NULL,
        active BOOLEAN NOT NULL DEFAULT TRUE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );"""

    products = """
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
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
        "regNo" TEXT,
        validUntil TEXT,
        classific TEXT,
        epd_url TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    );"""

    emission_factors = """
    CREATE TABLE IF NOT EXISTS emission_factors (
        emission_id SERIAL PRIMARY KEY,
        product_id INTEGER NOT NULL,
        "A1" REAL, "A2" REAL, "A3" REAL, "A1A2A3" REAL, "A4" REAL,
        "C1" REAL, "C2" REAL, "C3" REAL, "C4" REAL, "D" REAL,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );"""

    try:
        # Connect to Postgres
        conn = psycopg2.connect(**conn_params)
        create_database(conn, db_name)
        conn.close()

        # Connect to db
        conn_params["dbname"] = db_name
        conn = psycopg2.connect(**conn_params)

        create_table(conn, users)
        create_table(conn, projects)
        create_table(conn, products)
        create_table(conn, emission_factors)

        print(Fore.GREEN + "Creation of database tables SUCCEEDED")
        conn.close()

    except Error as e:
        print(Fore.RED + f"Error! Cannot create the database connection: {e}")

if __name__ == '__main__':
    main()
