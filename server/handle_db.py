import psycopg2
from psycopg2 import sql
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from colorama import Fore, init
import os
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), 'db_credentials.env')
load_dotenv(dotenv_path=env_path)

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

conn_params = {
    "dbname": db_name,
    "user": db_user,
    "password": db_password,
    "host": db_host,
    "port": db_port
}

def get_connection():
    return psycopg2.connect(**conn_params)

init(autoreset=True)

################################################################
######## USERS #################################################
################################################################


def add_user_to_db(data):
    """Accepts a dict containing name, email, password and 'photo_filename'
    Generates a password hash
    Inserts values (name, email, password_hash, photo_filename) to users 
    Returns a dict (user_id, name, email, password, password_hash, photo_filename)
    """
    name = data.get('name')
    email = data.get('email')
    photo_filename = data.get('photo_filename')
    password = data.get('password')
    password_hash = generate_password_hash(password)

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Check if email already exists
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cur.fetchone():  # retrieves one datapoint if found; else None
            print(Fore.RED + f'add_user_to_db FAILED for: {data["name"]}: "Email already registered.')
            return {"status": "failed", "message": "Eposten er allerede i bruk."}

        # If not; add the user
        cur.execute("""
        INSERT INTO users (name, email, password_hash, photo_filename)
        VALUES (%s, %s, %s, %s)
        RETURNING user_id;
        """, (name, email, password_hash, photo_filename))
        conn.commit()

        # Retrieve the last inserted row ID and return the result and a status message
        data["user_id"] = cur.fetchone()[0]
        data["projects"] = []
        message = f'add_user_to_db SUCCEEDED for: {data["name"]}'
        return {"status": "success", 'message': message, "user_data": data}

    except Exception as e:
        print(Fore.RED + f'add_user_to_db FAILED for: {data["name"]}. Error: {e}')
        return {"status": 'failed', "message": "Vi har for tiden problemer med systemet vårt. Vennligst prøv igjen senere"}
    
    finally:
        if conn:
            conn.close()

def get_userdata_from_db(col, value):
    """Retrieves userdata for a given user based on input search parameters
    Params: col: the attribute searched (e.g. 'email')
    value: the value searched for (e.g. a.a@a)
    returns user-data (name, email, password_hash, photo_filename); or None,
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = sql.SQL("SELECT * FROM users WHERE {} = %s").format(sql.Identifier(col))
        cur.execute(query, (value,))
        user = cur.fetchone()

        if user is None:
            print(Fore.RED + "User not found")
            return {"status": "failed", "message": "Brukeren ble ikke funnet"}

        user = dict(zip([desc[0] for desc in cur.description], user))
        user['status'] = 'success'
        user['message'] = 'get_userdata_from_db SUCCEEDED'
        return user

    except Exception as e:
        print(Fore.RED + f"get_userdata_from_db FAILED: {e}")
        return {"status": "failed", "message": "Vi har for tiden probelemer med systemet vårt. Venligst prøv igjen senere"}
    finally:
        if conn:
            conn.close()

def validate_and_return_user_data(data):
    """Args: data (dict) containing (email, password)
    Calls get_userdata_from_db, which returns (name, email, password_hash, photo_filename) if found; else None,
    Returns (name, email, photo_filename, and project_list) if found; else None,
    """
    email = data['email']
    password = data['password']

    user = get_userdata_from_db('email', email)
    if user["status"] == "failed":
        return user

    if not check_password_hash(user['password_hash'], password):
        return {'status': "failed", "message": "Incorrect password"}

    user_data = {k: v for k, v in user.items() if k != 'password_hash'}
    user_data['projects'] = get_project_data_from_db(user_data['user_id'])
    user_data['status'] = 'success'

    return user_data


################################################################
######## PROJECTS ##############################################
################################################################


def get_project_data_from_db(user_id):
    """Retrieves all project data for a given user_id from the database.
    Converts the project rows into dictionaries and fetches associated product data for each project.
    Returns a list of dictionaries containing project data.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Fetches project details
        cur.execute("SELECT * FROM projects WHERE user_id = %s", (user_id,))
        projects = cur.fetchall()
        
        if not projects:
            print(Fore.RED + f'No project data found for user_id: {user_id}')
            return []

        # Converts to dict, appends list of product data, and returns the result
        project_data = [dict(zip([desc[0] for desc in cur.description], project)) for project in projects]
        for project in project_data:
            get_product_data(project, conn)
            print(Fore.GREEN + f'project_data added for user_id: {user_id}, project_id: {project["project_id"]}')
        return project_data
    
    except Exception as e:
        print(Fore.RED + f"get_project_data_from_db: Failed to connect to db or execute query: {e}")
        return []
    
    finally:
        if conn:
            conn.close()

def add_project_to_db(project_data):
    """Adds a new project to the db table projects
    Params: ['user_id', 'name', 'type', 'bta', 'prosjektstart', 'analyseperiode', 'address', 
    'created_date', 'updated_date', 'active', AND (Optional) 'projects']
    Returns an updated project_data-dict including a status message indicating success or failure.
    """ 
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO projects (user_id, name, type, bta, prosjektstart, analyseperiode, address, created_date, updated_date, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING project_id;
        """, (
            project_data['user_id'], project_data['name'], project_data['type'], project_data['bta'], 
            project_data['prosjektstart'], project_data['analyseperiode'], project_data['address'], 
            project_data['created_date'], project_data['updated_date'], project_data['active']
        ))
        project_data['project_id'] = cur.fetchone()[0]

        # If the project contains products (e.g. is a copy); add products to db and update its products property
        if 'products' in project_data:
            updated_products = []
            for product in project_data['products']:
                product['project_id'] = project_data['project_id']
                product_data = add_product_to_db(product, conn)
                updated_products.append(product_data)
                print(Fore.GREEN + f'Added product_id: {product_data["product_id"]}') 
            project_data['products'] = updated_products

        conn.commit()
        print(Fore.GREEN + f'add_project_to_db SUCCEEDED for user_id: {project_data["user_id"]}, project name: {project_data["name"]}')
        return {'project_id': project_data['project_id'], "status": "success", 'data': project_data}

    except Exception as e:
        print(Fore.RED + f'add_project_to_db FAILED for: {project_data["name"]}. Error: {e}')
        return {"status": 'failed', "message": f"DB Error: {e}"}
    
    finally:
        if conn:
            conn.close()

def update_project_date(project_id, conn):
    """Updates the 'updated_date' of a project in the projects table.
    Args: conn (psycopg2.Connection): The database connection object.
    project_id (int): The ID of the project to update.
    update_date (str): The new update date to set.
    """
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d.%m.%Y')

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE projects SET updated_date = %s WHERE project_id = %s
        """, (formatted_date, project_id))
        conn.commit()

    except Exception as e:
        print(Fore.RED + f"update_project_date: Failed to connect to db or execute query: {e}")

def update_project_data(project_data):
    """Updates the project data of a given project.
    Params: project_data the data that will replace the existing data
    Returns a status message indicating success or failure.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Update the project details in the Projects table
        cur.execute("""
            UPDATE projects
            SET user_id = %s, name = %s, type = %s, bta = %s, prosjektstart = %s, 
            analyseperiode = %s, address = %s, created_date = %s, updated_date = %s, active = %s
            WHERE project_id = %s
        """, (
            project_data['user_id'], project_data['name'], project_data['type'],
            project_data['bta'], project_data['prosjektstart'], project_data['analyseperiode'],
            project_data['address'], project_data['created_date'], project_data['updated_date'],
            project_data['active'], project_data['project_id']
        ))

        conn.commit()
        print(Fore.GREEN + f'update_project_data SUCCEEDED for: {project_data["name"]}')
        return {"status": "success", "message": "Project data updated successfully."}

    except Exception as e:
        print(Fore.RED + f"Failed to update project data: {e}")
        return {"status": "failed", "message": str(e)}
    finally:
        if conn:
            conn.close()

def delete_project_data(project_id):
    """Deletes any data in 'projects', 'products' and 'emission_factors' for a given project_id
    Returns a status message indicating success or failure.
    """
    print(Fore.YELLOW + f'delete_project_data called for project_id: {project_id}')
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Retrieve the product_ids associated with the project and delete them
        cur.execute("SELECT product_id FROM products WHERE project_id = %s", (project_id,))
        product_ids = cur.fetchall()
        for product_id in product_ids:
            delete_product_data(product_id[0], conn)

        # Delete project details FROM projects table
        cur.execute("DELETE FROM projects WHERE project_id = %s", (project_id,))
        project_rows_deleted = cur.rowcount
        conn.commit()

        # Return status message indicating whether or not any data was deleted
        if project_rows_deleted > 0:
            print(Fore.GREEN + f'delete_project_data SUCCEEDED for project ID: {project_id}; entries deleted: {project_rows_deleted}')
            return {"status": "success", "message": f"prosjektnr {project_id} er slettet"}
        else:
            print(Fore.RED + f'delete_project_data FAILED: No project found with ID {project_id}')
            return {"status": "failed", "message": f"prosjektnr {project_id} ble ikke funnet"}

    except Exception as e:
        message = f"delete_project_data: Failed to connect to db or execute query: {e}"
        print(Fore.RED + message)
        return {"status": "failed", "message": message}
    finally:
        if conn:
            conn.close()


################################################################
######## PRODUCTS ##############################################
################################################################


def get_product_data(project, conn):
    """Retrieves product data for each product belonging to a given project
    Params: projects: includes minimum project_id
    """
    try:
        # Retrieve product data for each project
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE project_id = %s", (project['project_id'],))
        products = cur.fetchall()
        project['products'] = [dict(zip([desc[0] for desc in cur.description], product)) for product in products]

        # Retrieve emission factors for each product
        for product in project['products']:
            cur.execute("SELECT * FROM emission_factors WHERE product_id = %s", (product['product_id'],))
            emission_factors = cur.fetchall()
            product['emission_factors'] = dict(zip([desc[0] for desc in cur.description], emission_factors[0])) if emission_factors else {}

    except Exception as e:
        print(Fore.RED + f'get_product_data FAILED: {e}')

    finally:
        if cur:
            cur.close()

def add_product_to_db(product_data, conn=None):
    """Params: ['bygningsdel', 'produktgruppe', 'name', 'displayedName', 'type', 'utskiftingsintervall', 'vedlikeholdsutslipp',
        'quantity', 'unit', 'emission_factors', 'classific', 'owner', 'regNo', 'uuid', 'validUntil', 'project_id', epd_url]
    Returns updated product_data
    """
    print(f'add_product_to_db called for project_id {product_data["project_id"]}; for product_name: {product_data["name"]}')
    try:
        # Close after execution if the function establishes its own connection
        local_conn = conn is None
        if conn is None:
            conn = get_connection()
        cur = conn.cursor()

        # Insert the new product
        cur.execute("""
            INSERT INTO products (project_id, quantity, unit, bygningsdel, produktgruppe, utskiftingsintervall, vedlikeholdsutslipp, type, uuid, owner, name, "regNo", validUntil, classific, epd_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING product_id;
        """, (
            product_data['project_id'], product_data['quantity'], product_data['unit'], product_data['bygningsdel'], 
            product_data['produktgruppe'], product_data['utskiftingsintervall'], product_data['vedlikeholdsutslipp'], 
            product_data['type'], product_data['uuid'], product_data['owner'], product_data['name'], product_data['regNo'], 
            product_data['validUntil'], product_data['classific'], product_data['epd_url']
        ))
        product_id = cur.fetchone()[0]
        print(f'add_product_to_db -> product_id: {product_id}')

        # Add emission data to db and update project.updated_date for the active project
        update_project_date(product_data['project_id'], conn)
        add_emission_factors_to_db(product_data, product_id, conn)
        conn.commit()
        
        # Construct and return the added product
        new_product = {
            **product_data,
            'product_id': product_id,
            'status': 'success',
        }
        print(Fore.GREEN + f'add_product_to_db SUCCEEDED for: {product_data["name"]}')
        return new_product

    except Exception as e:
        print(Fore.RED + f"add_product_to_db: FAILED to connect to db or execute query: {e}")
        return {"status": "failed"}

    finally:
        if conn and local_conn:
            conn.close()

def validate_product_for_update(product_id):
    """Retrieves the project_id of the associated project and checks if it is in session
    Returns a status message indicating success or failure.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Validate that the product belongs to a projects belonging to the user in session
        cur.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cur.fetchone()
        if product is None:
            return {"status": "failed", "message": "No product found with given ID", "code": 400}

        project_id = product[1]
        if project_id not in session.get('project_ids', []):
            return {"status": "failed", "message": "User lacks the rights to delete this product", "code": 401}
        
        return {"status": "success", 'project_id': project_id}
        
    except Exception as e:
        message = f"validate_product_for_update: Failed to connect to db or execute query: {e}"
        return {"status": "failed", "message": message, "code": 404}

    finally:
        if conn:
            conn.close()

def update_product_data(product_data):
    """ Updates the details of a product in the database.
    Params: product_data dictionary containing product details and updates the corresponding row in the Products table.
    If emission factors are provided, updates them as well.
    Returns a status message indicating success or failure.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Update the product details in the Products table
        cur.execute("""
            UPDATE products
            SET project_id = %s, quantity = %s, unit = %s, bygningsdel = %s, produktgruppe = %s, 
            utskiftingsintervall = %s, vedlikeholdsutslipp = %s, type = %s, uuid = %s, owner = %s, 
            name = %s, "regNo" = %s, validUntil = %s, classific = %s, epd_url = %s
            WHERE product_id = %s
        """, (
            product_data['project_id'], product_data['quantity'], product_data['unit'], product_data['bygningsdel'], 
            product_data['produktgruppe'], product_data['utskiftingsintervall'], product_data['vedlikeholdsutslipp'], 
            product_data['type'], product_data['uuid'], product_data['owner'], product_data['name'], product_data['regNo'],
            product_data['validUntil'], product_data['classific'], product_data['epd_url'], product_data['product_id'] 
        ))

        # Check if emission factors are provided and update them
        if 'emission_factors' in product_data:
            update_emission_factors(conn, product_data['product_id'], product_data['emission_factors'])
        else:
            print(Fore.RED + 'update_product_data: NB! Emission factors missing!!')

        update_project_date(product_data['project_id'], conn)

        conn.commit()
        print(Fore.GREEN + f'update_product_data SUCCEEDED for: {product_data["name"]}')
        return {"status": "success"}

    except Exception as e:
        print(Fore.RED + f"update_product_data: Failed to connect to db or execute query: {e}")
        return {"status": "failed"}

    finally:
        if conn:
            conn.close()

def delete_product_data(product_id, conn=None):
    """Deletes any data in tables 'products' and 'emission_factors' and with a given product_id.
    Returns a status message indicating success or failure.
    """
    print(f'delete_product_data called for product_id: {product_id}')
    try:
        local_conn = conn is None
        if conn is None:
            conn = get_connection()
        cur = conn.cursor()

        # Retrieves the project_id
        cur.execute("SELECT project_id FROM products WHERE product_id = %s", (product_id,))
        project = cur.fetchone()
        project_id = project[0]

        # Delete product from tables products and emission_factors
        cur.execute("DELETE FROM emission_factors WHERE product_id = %s", (product_id,))
        cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        products_deleted = cur.rowcount
        conn.commit()

        # If deletions were successful; update project_date and return a success message
        if products_deleted > 0:
            update_project_date(project_id, conn)
            message = f'delete_product_data SUCCEEDED for product ID: {product_id}'
            return {"status": "success", "message": message}
        else:
            message = f'delete_product_data FAILED: No product found with ID {product_id}'
            return {"status": "failed", "message": message}

    except Exception as e:
        message = f"delete_product_data: FAILED to connect to db or execute query: {e}"
        return {"status": "failed", "message": message}

    finally:
        if conn and local_conn:
            conn.close()


################################################################
######## EMISSION FACTORS ######################################
################################################################

def add_emission_factors_to_db(product_data, product_id, conn):
    """Adds emission factors to the database for a given product.
    If emission factors are not provided in product_data, logs a message and returns.
    Converts emission factors to float before returning.
    """
    if 'emission_factors' not in product_data:
        print(Fore.RED + 'add_emission_factors_to_db: emission data missing!')
        return
    
    emission_factors = product_data['emission_factors']
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO emission_factors (product_id, "A1", "A2", "A3", "A1A2A3", "A4", "C1", "C2", "C3", "C4", "D")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            product_id, 
            emission_factors['A1'], emission_factors['A2'], emission_factors['A3'], emission_factors['A1A2A3'], 
            emission_factors['A4'], emission_factors['C1'], emission_factors['C2'], 
            emission_factors['C3'], emission_factors['C4'], emission_factors['D']
        ))

        # Convert emission factors to float before returning
        product_data['emission_factors'] = {key: float(value) for key, value in emission_factors.items()}
        conn.commit()

    except Exception as e:
        print(Fore.RED + f"Failed to add emission factors: {e}")
        return {"status": "failed", "message": str(e)}
    finally:
        if cur:
            cur.close()

def update_emission_factors(conn, emission_factors, product_id):
    """Updates the emission factors of a given product.
    If an error occurs during the update, logs the error and returns a failure message.
    """
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE emission_factors
            SET "A1" = %s, "A2" = %s, "A3" = %s, "A4" = %s, "C1" = %s, "C2" = %s, "C3" = %s, "C4" = %s, "D" = %s
            WHERE product_id = %s
        """, (
            emission_factors['A1'], emission_factors['A2'], emission_factors['A3'], 
            emission_factors['A4'], emission_factors['C1'], emission_factors['C2'], 
            emission_factors['C3'], emission_factors['C4'], emission_factors['D'],
            product_id
        ))

        conn.commit()

    except Exception as e:
        print(Fore.RED + f"Failed to update emission factors: {e}")
        return {"status": "failed", "message": str(e)}
    finally:
        if cur:
            cur.close()