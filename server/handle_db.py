import sqlite3
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Establish connection to db
def get_db_connection():
    conn = sqlite3.connect('userdata.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_current_date():
    # Get the current date
    current_date = datetime.now()
    formatted_date = str(current_date.strftime('%d.%m.%Y'))
    return formatted_date


################################################################
######## USERS #################################################
################################################################


def add_user_to_db(data):
    """" Accepts a dict containing name, email, password and 'photo_filename'
    Generates a password hash
    Posts values (name, email, password_hash, photo_filename) to Users 
    returns a dict (user_id, name, email, password, password_hash, photo_filename)
    """
    name = data.get('name', None)
    email = data.get('email', None)
    photo_filename = data.get('photo_filename', None)
    password = data.get('password', None)
    password_hash = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if email already exists
        cur.execute("SELECT email FROM Users WHERE email = ?", (email,))
        if cur.fetchone(): # retrieves one datapoint if found; else None
            print(f'add_user_to_db FAILED for: {data["name"]}: "Email already registered.')
            return {"status": "failed", "message": "Eposten er allerede i bruk."}

        # If not; add the user
        cur.execute("""
        INSERT INTO Users (name, email, password_hash, photo_filename)
        VALUES (?, ?, ?, ?)
        """, (name, email, password_hash, photo_filename))
        conn.commit()

        data["user_id"] = cur.lastrowid
        data["projects"] = []
        message = f'add_user_to_db SUCCEEDED for: {data["name"]}'
        return {"status": "success", 'message': message, "user_data": data }

    except Exception as e:
        print(f'add_user_to_db FAILED for: {data["name"]}. Error: {e}')
        return {"status": 'failed', "message": "Vi har for tiden probelemer med systemet vårt. Venligst prøv igjen senere"}
    
    finally:
        if conn:
            conn.close()


def get_userdata_from_db(col, value):
    """" col: the attribute searched (e.g. 'email')
    value: the value searched for (e.g. a.a@a)
    returns user-data (name, email, password_hash, photo_filename); or None, 
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Users WHERE {col} = ?", (value,))
        user = cur.fetchone()

        if user is None:
            print("User not found")
            return {"status": "failed", "message": "Brukeren ble ikke funnet"}
        
        user = dict(user)
        user['status'] = 'success'
        user['message'] = 'get_userdata_from_db SUCCEEDED'
        return user
        
    except Exception as e:
        print(e)
        return {"status": "failed", "message": str(e)}

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
    print(user)

    if user["status"] == "failed":
        return user
   
    if not check_password_hash(user['password_hash'], password):
        return {'status': "failed", "message": "Incorrect password"}
    
    user_data = {k:v for k, v in user.items() if k != 'password_hash'}
    user_data['projects'] = get_project_data_from_db(user_data['user_id'])
    user_data['status'] = 'success'

    return user_data


################################################################
######## PROJECTS ##############################################
################################################################


def get_project_data_from_db(user_id):
    try:
        conn = sqlite3.connect('userdata.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Fetch project details
        cur.execute("""SELECT * FROM Projects WHERE user_id = ?""", (user_id,))
        projects = cur.fetchall()
        
        if not projects:
            print('No project data found!')
            return []

        project_data  = [dict(project) for project in projects]
        for project in project_data:
            get_product_data(project, conn)

        print('emission_factors_added')
        return project_data
    
    except Exception as e:
        print(f"get_project_data_from_db: Failed to connect to db or execute query: {e}")
        return []
    
    finally:
        if conn:
            conn.close()


def add_project_to_db(data):
    """Args: ['user_id', 'name', 'type', 'bta', 'prosjektstart', 'analyseperiode', 'address', 
    'created_date', 'updated_date', 'active', AND (Optional) 'projects']"""

    # TODO: SJEKK OM JEG TRENGER DENNE KODEN
    # user_data = get_userdata_from_db('user_id', user_id)
    # if user_data["status"] == "failed":
    #     print(f'add_project_to_db FAILED for: {data["name"]}. User_id not found')
    #     return {"status": "failed"}

    try:
        with sqlite3.connect('userdata.db') as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Projects (user_id, name, type, bta, prosjektstart, analyseperiode, address, created_date, updated_date, active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['user_id'], data['name'], data['type'], data['bta'], data['prosjektstart'],
                data['analyseperiode'], data['address'], data['created_date'], data['updated_date'], data['active']
            ))
            # TODO: SE UNDER
            # project_id = cur.lastrowid

            if 'products' in data:
                for product in data['products']:
                    print(product) # TODO: SJEKK OM PROJECT_ID KOMMER MED; ELLERS -> product['project_id'] = project_id
                    add_product_to_db(product)

            print(f'add_project_to_db SUCCEEDED for: {data["name"]}')
            return {'project_id': cur.lastrowid, "status": "success"}

    except Exception as e:
        print(f'add_project_to_db FAILED for: {data["name"]}. Error: {e}')
        return {"status": 'failed', "message": f"DB Error: {e}"}


def update_project_date(conn, project_id):
    """Updates the 'updated_date' of a project in the Projects table.
    Args: conn (sqlite3.Connection): The database connection object.
    project_id (int): The ID of the project to update.
    update_date (str): The new update date to set.
    """
    current_date = datetime.now()
    formatted_date = str(current_date.strftime('%d.%m.%Y'))

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Projects SET updated_date = ? WHERE project_id = ?
        """, (formatted_date, project_id))

    except Exception as e:
        print(f"update_project_date prints: Failed to connect to db or execute query: {e}")


def update_project_data(project_data):
    try:
        conn = sqlite3.connect('userdata.db')
        cur = conn.cursor()

        # Update the project details in the Projects table
        cur.execute("""
            UPDATE Projects
            SET user_id = ?, name = ?, type = ?, bta = ?, prosjektstart = ?, 
            analyseperiode = ?, address = ?, created_date = ?, updated_date = ?, active = ?
            WHERE project_id = ?
        """, (
            project_data['user_id'], project_data['name'], project_data['type'],
            project_data['bta'], project_data['prosjektstart'], project_data['analyseperiode'],
            project_data['address'], project_data['created_date'], project_data['updated_date'],
            project_data['active'], project_data['project_id']
        ))

        conn.commit()
        print(f'update_project_data SUCCEEDED for: {project_data["name"]}')
        return {"status": "success", "message": "Project data updated successfully."}

    except Exception as e:
        print(f"Failed to update project data: {e}")
        return {"status": "failed", "message": str(e)}

    finally:
        if conn:
            conn.close()


def delete_project_data(project_id):
    """Deletes any data in 'Projects' and 'Products' with a given project_id
    Returns 'success' if any data was found; else returns 'failed'
    """
    print(f'delete_project_data called for {project_id}')
    try:
        conn = sqlite3.connect('userdata.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM Projects WHERE project_id = ?", (project_id,))
        project_rows_deleted = cur.rowcount
        conn.commit()

        if project_rows_deleted > 0:
            print(f'Delete_project_data SUCCEEDED for project ID: {project_id}')
            print(f'Deleted {project_rows_deleted} entries from Projects')
            return {"status": "success"}
        else:
            print(f'Delete_project_data FAILED: No project found with ID {project_id}')
            return {"status": "failed"}

    except Exception as e:
        print(f"delete_project_data: Failed to connect to db or execute query: {e}")
        return {"status": "failed"}

    finally:
        if conn:
            conn.close()


################################################################
######## PRODUCTS ##############################################
################################################################


def get_product_data(project, conn):
    # Retrieve product data for each project
    cur = conn.cursor()
    try:
        # Retrieve product data for each project
        cur.execute("SELECT * FROM Products WHERE project_id = ?", (project['project_id'],))
        products = cur.fetchall()
        project['products'] = [dict(product) for product in products]

        for product in project['products']:
            print(product)

        # Retrieve emission factors for each product
        for product in project['products']:
            cur.execute("SELECT * FROM EmissionFactors WHERE product_id = ?", (product['product_id'],))
            emission_factors = cur.fetchall()
            print(emission_factors)
            product['emission_factors'] = dict(emission_factors[0]) if emission_factors else {} 

    finally:
        cur.close()
       

def add_product_to_db(product_details):
    """ARG: ['bygningsdel', 'produktgruppe', 'name', 'displayedName', 'type', 'utskiftingsintervall', 'vedlikeholdsutslipp',
      'quantity', 'unit', 'emission_factors', 'classific', 'owner', 'regNo', 'uuid', 'validUntil', 'project_id', EPD_URL]"""
    try:
        with sqlite3.connect('userdata.db') as conn: # context manager
            cur = conn.cursor()

            # Insert the new product
            cur.execute("""
                INSERT INTO Products (project_id, quantity, unit, bygningsdel, produktgruppe, utskiftingsintervall, vedlikeholdsutslipp, type, uuid, owner, name, regNo, validUntil, classific, EPD_URL)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_details['project_id'], product_details['quantity'], product_details['unit'],
                product_details['bygningsdel'], product_details['produktgruppe'], product_details['utskiftingsintervall'], 
                product_details['vedlikeholdsutslipp'], product_details['type'], product_details['uuid'], 
                product_details['owner'], product_details['name'], product_details['regNo'], 
                product_details['validUntil'], product_details['classific'], product_details['EPD_URL']
            ))
            product_id = cur.lastrowid

            # Add emission data to db and update project.updated_date for the active project
            update_project_date(conn, product_details['project_id'])
            add_emission_factors_to_db(conn, product_details, product_id)
            
            # Construct and return the added product
            new_product = {
                **product_details,
                'product_id': product_id,
                'status': 'success',
            }
            print(f'add_product_to_db SUCCEEDED for: {product_details["name"]}')
            return new_product

    except Exception as e:
        print(f"add_product_to_db: Failed to connect to db or execute query: {e}")
        return {"status": "failed"}


def validate_product_for_update(product_id):
    try:
        conn = sqlite3.connect('userdata.db')
        cur = conn.cursor()

        # Validate that the product belongs to a projects belonging to the user in session
        cur.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,))
        product = cur.rowcount
        if product is None:
            return {"status": "failed", "message": "No product found with given ID", "code": 400}

        project_id = product[0]
        if project_id not in session.get('project_ids', []):
            return {"status": "failed", "message": "User lacks the rights to delete this product", "code": 401}
        
        return {"status": "success", 'project_id': project_id}
        
    except Exception as e:
        message = f"validate_product_for_update: Failed to connect to db or execute query: {e}"
        return {"status": "success", "message": message, "code": 404}

    finally:
        if conn:
            conn.close()


def update_product_data(product_details):
    try:
        conn = sqlite3.connect('userdata.db')
        cur = conn.cursor()

        # Update the product details in the Products table
        cur.execute("""
            UPDATE Products
            SET project_id = ?, quantity = ?, unit = ?, bygningsdel = ?, produktgruppe = ?, 
            utskiftingsintervall = ?, vedlikeholdsutslipp = ?, type = ?, uuid = ?, owner = ?, 
            name = ?, regNo = ?, validUntil = ?, classific = ?, EPD_URL = ?
            WHERE product_id = ?
        """, (
            product_details['project_id'], product_details['quantity'], product_details['unit'], product_details['bygningsdel'], 
            product_details['produktgruppe'], product_details['utskiftingsintervall'], product_details['vedlikeholdsutslipp'], 
            product_details['type'], product_details['uuid'], product_details['owner'], product_details['name'], 
            product_details['regNo'], product_details['validUntil'], product_details['classific'], product_details['EPD_URL'],
            product_details['product_id'] 
        ))
        conn.commit()

        # Check if emission factors are provided and update them
        if 'emission_factors' in product_details:
            update_emission_factors(conn, product_details['product_id'], product_details['product_id'])
        else:
            print('update_product_data: NB! updateDate missing!!')       

        update_project_date(conn, product_details['project_id'])
        print(f'update_product_data SUCCEEDED for: {product_details["name"]}')
        return {"status": "success"}

    except Exception as e:
        print(f"update_product_data: Failed to connect to db or execute query: {e}")
        return {"status": "failed"}

    finally:
        if conn:
            conn.close()


def delete_product_data(product_id):
    """For a given product_id:
    Deletes any data in 'EmissionFactors' and 'Products' with that product_id
    Returns 'success' if any data was found and user has rights; else returns 'failed'
    """
    try:
        conn = sqlite3.connect('userdata.db')
        cur = conn.cursor()

        #  Delete product from both Products and EmissionFactors
        cur.execute("DELETE FROM EmissionFactors WHERE product_id = ?", (product_id,))
        project = cur.fetchone()  # Fetch the first row of the result
        project_id = project[0] 

        cur.execute("DELETE FROM Products WHERE product_id = ?", (product_id,))
        conn.commit()

        # Check if deletions were successful
        if cur.rowcount > 0:
            update_project_date(conn, project_id)
            message = f'Delete_product_data SUCCEEDED for product ID: {product_id}'
            return {"status": "success", "message": message}
        else:
            message = f'Delete_product_data FAILED: No product found with ID {product_id}'
            return {"status": "success", "message": message}

    except Exception as e:
        message = f"delete_product_data: Failed to connect to db or execute query: {e}"
        return {"status": "success", "message": message}

    finally:
        if conn:
            conn.close()


################################################################
######## EMISSION FACTORS ######################################
################################################################


def add_emission_factors_to_db(conn, product_details, product_id):
     # Check if emission factors are provided and insert them
    if 'emission_factors' not in product_details:
        print('add_emission_factors_to_db posts: emission data missing!')
        return
    
    emission_factors = product_details['emission_factors']
    print(emission_factors)
    
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO EmissionFactors (product_id, A1, A2, A3, A1A2A3, A4, C1, C2, C3, C4, D)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_id, 
        emission_factors['A1'], emission_factors['A2'], emission_factors['A3'], emission_factors['A1A2A3'], 
        emission_factors['A4'], emission_factors['C1'], emission_factors['C2'], 
        emission_factors['C3'], emission_factors['C4'], emission_factors['D']
    ))

    # Convert emission factors to float before returning
    product_details['emission_factors'] = {key: float(value) for key, value in emission_factors.items()}


def update_emission_factors(conn, emission_factors, product_id):
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE EmissionFactors
            SET A1 = ?, A2 = ?, A3 = ?, A4 = ?, C1 = ?, C2 = ?, C3 = ?, C4 = ?, D = ?
            WHERE product_id = ?
        """, (
            emission_factors['A1'], emission_factors['A2'], emission_factors['A3'], 
            emission_factors['A4'], emission_factors['C1'], emission_factors['C2'], 
            emission_factors['C3'], emission_factors['C4'], emission_factors['D'],
            product_id
        ))

        conn.commit()

    except Exception as e:
        print(f"Failed to update emission factors: {e}")
        return {"status": "failed", "message": str(e)}


# TESTING #

def initialize_db_with_data(json_data):
    # Assuming json_data is a dictionary already
    for user in json_data['users']:
        add_user_to_db(user)

    for project in json_data['projects']:
        add_project_to_db(project)
    
    for product in json_data['products']:
        add_product_to_db(product)

if __name__ == '__main__':
    # Open and read the JSON file
    with open('data.json', 'r') as file:
        json_data = json.load(file)  # This loads JSON data as a Python dictionary

    # Pass the dictionary to the function
    initialize_db_with_data(json_data)
