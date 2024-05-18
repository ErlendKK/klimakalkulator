import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

# Establish connection to db
def get_db_connection():
    conn = sqlite3.connect('userdata.db')
    conn.row_factory = sqlite3.Row
    return conn


def add_userdata_to_db(data):
    """" Accepts a dict containing name, email, password and 'photo_filename'
    Generates a password hash
    Posts values (name, email, password_hash, photo_filename) to Users 
    returns a dict (user_id, name, email, password, password_hash, photo_filename)
    """
    name = data.get('name', None)
    email = data.get('email', None)
    password = data.get('password', None)
    photo_filename = data.get('photo_filename', None)
    password_hash = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if email already exists
        cur.execute("SELECT email FROM Users WHERE email = ?", (email,))
        if cur.fetchone(): # retrieves one datapoint if found; else None
            print(f'add_userdata_to_db FAILED for: {data["name"]}: "Email already registered.')
            return {"status": "failed", "message": "En bruker er allerede registrert med denne epostadressen."}

        # If not; add the user
        cur.execute("""
        INSERT INTO Users (name, email, password_hash, photo_filename)
        VALUES (?, ?, ?, ?)
        """, (name, email, password_hash, photo_filename))
        conn.commit()

        data["user_id"] = cur.lastrowid
        print(f'add_userdata_to_db SUCCEEDED for: {data["name"]}')
        return {"status": "success", "user_data": data }

    except Exception as e:
        print(f'add_userdata_to_db FAILED for: {data["name"]}. Error: {e}')
        return {"status": 'failed', "message": "Vi har for tiden probelmer med systemet vårt. Venligst prøv igjen senere"}
    
    finally:
        if conn:
            conn.close()


def get_userdata_from_db(col, value):
    """" col: the attribute searched (e.g. 'email')
    value: the value searched for (e.g. a.a@a)
    returns one user-datapoint (name, email, password_hash, photo_filename); or None, 
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Users WHERE {col} = ?", (value,))
        user = cur.fetchone()

        if user is None:
            print("User not found")
            return {"status": "failed", "message": "User not found"}
        
        user = dict(user)
        user['status'] = 'success'
        return user
        
    except Exception as e:
        print(e)
        return {"status": "failed", "message": str(e)}

    finally:
        if conn:
            conn.close()


def validate_and_return_user_data(data):
    """input argument data (email, password, )
    returns (name, email, photo_filename, and project_list) if found; else None, 
    """    
    email = data['email']
    password = data['password']
    # get_userdata_from_db returns (name, email, password_hash, photo_filename) if found; else None, 
    user = get_userdata_from_db('email', email)
    print(user)

    if user["status"] == "failed":
        print('validate_and_return_user_data failed to get the user')
        return user
   
    if not check_password_hash(user['password_hash'], password):
        return {'status': "failed", "message": "Incorrect password"}
    
    user_data = {k:v for k, v in user.items() if k != 'password_hash'}
    user_data['projects'] = get_project_data(user_data['user_id'])
    user_data['status'] = 'success'

    return user_data


def get_project_data(user_id):
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

        return project_data
    
    except Exception as e:
        print(f"Failed to connect to db or execute query: {e}")
        return []
    
    finally:
        if conn:
            conn.close()


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
            product['emission_factors'] = dict(emission_factors[0]) if emission_factors else {} 

    finally:
        cur.close()
    
    

def post_project_to_db(data):
    user_id = data['user_id']
    name = data['name']
    type = data['type']
    bta = data['bta']
    prosjektstart = data['prosjektstart']
    analyseperiode = data['analyseperiode']
    address = data['address']
    created_date = data['created_date']
    updated_date = data['updated_date']
    active = data['active']

    user_data = get_userdata_from_db('user_id', user_id)
    if user_data["status"] == "failed":
        print(f'post_project_to_db FAILED for: {data["name"]}. User_id not found')
        return {"status": "failed"}
    
    user_id = user_data["user_id"]

    # Connect to db
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO Projects (user_id, name, type, bta, prosjektstart, analyseperiode, address, created_date, updated_date, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, name, type, bta, prosjektstart, analyseperiode, address, created_date, updated_date, active))
        conn.commit()

        print(f'post_project_to_db SUCCEEDED for: {data["name"]}')
        return {'project_id': cur.lastrowid, "status": "success"}

    except Exception as e:
        print(f'post_project_to_db FAILED for: {data["name"]}. Error: {e}')
        return {"status": 'failed', "message": f"DB Error: {e}"}
    
    finally:
        if conn:
            conn.close()


def add_product_data(product_details):
    try:
        conn = sqlite3.connect('userdata.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print(product_details)

        # Insert the new product
        cur.execute("""
            INSERT INTO Products (project_id, quantity, unit, bygningsdel, produktgruppe, utskiftingsintervall, vedlikeholdsutslipp, type, uuid, owner, name, regNo, validUntil, classific)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_details['project_id'], product_details['quantity'], product_details['unit'],
            product_details['bygningsdel'], product_details['produktgruppe'], product_details['utskiftingsintervall'], 
            product_details['vedlikeholdsutslipp'], product_details['type'],
            product_details['uuid'], product_details['owner'], product_details['name'],
            product_details['regNo'], product_details['validUntil'], product_details['classific']
        ))
        product_id = cur.lastrowid

        # Check if emission factors are provided and insert them
        if 'emission_factors' in product_details:
            emission_factors = product_details['emission_factors']

            cur.execute("""
                INSERT INTO EmissionFactors (product_id, A1, A2, A3, A1A2A3, A4, C1, C2, C3, C4, D)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id, 
                emission_factors['A1'], emission_factors['A2'], emission_factors['A3'], emission_factors['A1A2A3'], 
                emission_factors['A4'], emission_factors['C1'], emission_factors['C2'], 
                emission_factors['C3'], emission_factors['C4'], emission_factors['D']
            ))

        conn.commit()

        # Convert emission factors to float before returning
        if 'emission_factors' in product_details:
            product_details['emission_factors'] = {key: float(value) for key, value in emission_factors.items()}

        # Construct and return the added product
        new_product = {
            **product_details,
            'product_id': product_id,
            'status': 'success',
        }
        print(f'add_product_data SUCCEEDED for: {product_details["name"]}')

        return new_product

    except Exception as e:
        print(f"Failed to connect to db or execute query: {e}")
        return {"status": "failed"}

    finally:
        if conn:
            conn.close()
        

def delete_product_data(product_id):
    """
    For a given product_id:
    Deletes any data in 'EmissionFactors' and 'Products' with that product_id
    Returns 'success' if any data was found; else returns 'failed'
    """
    try:
        conn = sqlite3.connect('userdata.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM EmissionFactors WHERE product_id = ?", (product_id,))
        emission_rows_deleted = cur.rowcount
        cur.execute("DELETE FROM Products WHERE product_id = ?", (product_id,))
        product_rows_deleted = cur.rowcount
        conn.commit()

        if product_rows_deleted > 0:
            print(f'Delete_product_data SUCCEEDED for product ID: {product_id}')
            print(f'Deleted {product_rows_deleted} entries from Products, and {emission_rows_deleted} entries from EmissionFactors')
            return {"status": "success"}
        else:
            print(f'Delete_product_data FAILED: No product found with ID {product_id}')
            return {"status": "failed"}

    except Exception as e:
        print(f"Failed to connect to db or execute query: {e}")
        return {"status": "failed"}

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
        print(f"Failed to connect to db or execute query: {e}")
        return {"status": "failed"}

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
            name = ?, regNo = ?, validUntil = ?, classific = ?
            WHERE product_id = ?
        """, (
            product_details['project_id'], product_details['quantity'], product_details['unit'],
            product_details['bygningsdel'], product_details['produktgruppe'], product_details['utskiftingsintervall'], 
            product_details['vedlikeholdsutslipp'], product_details['type'],
            product_details['uuid'], product_details['owner'], product_details['name'],
            product_details['regNo'], product_details['validUntil'], product_details['classific'],
            product_details['product_id'] 
        ))

        # Check if emission factors are provided and update them
        if 'emission_factors' in product_details:
            emission_factors = product_details['emission_factors']
            cur.execute("""
                UPDATE EmissionFactors
                SET A1 = ?, A2 = ?, A3 = ?, A4 = ?, C1 = ?, C2 = ?, C3 = ?, C4 = ?, D = ?
                WHERE product_id = ?
            """, (
                emission_factors['A1'], emission_factors['A2'], emission_factors['A3'], 
                emission_factors['A4'], emission_factors['C1'], emission_factors['C2'], 
                emission_factors['C3'], emission_factors['C4'], emission_factors['D'],
                product_details['product_id']
            ))

        conn.commit()
        print(f'update_product_data SUCCEEDED for: {product_details["name"]}')
        return {"status": "success"}

    except Exception as e:
        print(f"Failed to update product data: {e}")
        return {"status": "failed"}

    finally:
        if conn:
            conn.close()


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


#################
'''For testing'''
#################

users = [
    {
    'name': "Erlend",
    'email': 'a@a.a',
    'password': 'aaa',
    'photo_filename': 'profile-picture1.png',
    },
    {
    'name': "Anders",
    'email': 'b@b.b',
    'password': 'bbb',
    'photo_filename': 'profile-picture2.png',
    }
]

projects = [ 
    {
    'name': 'Innoasis', 
    'type': 'Kontor', 
    'bta': 5500,
    'prosjektstart': 2028,
    'analyseperiode': 50,
    'address': 'min adresse', 
    'created_date': '08.01.2023', 
    'updated_date': '29.06.2023', 
    'active': True, 
    'user_id': 1
    },
    {
    'name': 'Finansparken', 
    'type': 'Kontor', 
    'bta': 6500,
    'prosjektstart': 2025,
    'analyseperiode': 60,
    'address': 'min adresse2', 
    'created_date': '09.04.2023', 
    'updated_date': '09.04.2024', 
    'active': True, 
    'user_id': 1
    },
    {
    'name': 'Herbarium', 
    'type': 'Handel',
    'bta': 7800,
    'prosjektstart': 2014,
    'analyseperiode': 50,
    'address': 'min adresse3', 
    'created_date': '02.03.2021', 
    'updated_date': '01.01.2022', 
    'active': True, 
    'user_id': 1
    }
]

products = [ 
    {
    'project_id': 1,
    'quantity': 500,
    'unit': "m3",
    'uuid': 'some-uuid1',
    'owner': 'Jærbetong',
    'name': 'Stedstøpt Betong',
    'displayedName': 'Stedstøpt Betong',
    'regNo': 'some regNo1',
    'utskiftingsintervall': 50,
    'vedlikeholdsutslipp': 1,
    'validUntil': '2024',
    'classific': 'some classification1',
    'bygningsdel': "Dekker (25)",
    'produktgruppe': "Dekker (225)",
    'type': "Betong",
    'emission_factors':
        {
            'product_id': 1,
            'A1': 5,
            'A2': 7,
            'A3': 3,
            'A4': 2,
            'C1': 1,
            'C2': 2,
            'C3': 3,
            'C4': 2,
            'D': 1,
            'A1A2A3': 0
        }
    },

    {
    'project_id': 1,
    'quantity': 500,
    'unit': "m3",
    'uuid': 'some-uuid2',
    'owner': 'Jærbetong',
    'name': 'Påstøp',
    'displayedName': 'Stedstøpt Betong',
    'regNo': 'some regNo2',
    'utskiftingsintervall': 20,
    'vedlikeholdsutslipp': 4,
    'validUntil': '2024',
    'classific': 'some classification2',
    'bygningsdel': "Dekker (25)",
    'produktgruppe': "Dekker (225)",
    'type': "Isolasjon",
    'emission_factors':
        {
            'product_id': 2,
            'A1': 2,
            'A2': 3,
            'A3': 4,
            'A4': 5,
            'C1': 2,
            'C2': 3,
            'C3': 5,
            'C4': 1,
            'D': 2,
            'A1A2A3': 0
        },
    },

    {
    'project_id': 1,
    'quantity': 500,
    'unit': "m3",
    'uuid': 'some-uuid3',
    'owner': 'Glava',
    'name': 'Glassull',
    'displayedName': 'Stedstøpt Betong',
    'regNo': 'some regNo3',
    'utskiftingsintervall': 40,
    'vedlikeholdsutslipp': 0,
    'validUntil': '2024',
    'classific': 'some classification3',
    'bygningsdel': "Innervegger (24)",
    'produktgruppe': "Innvendige overflater og kledninger (246)",
    'type': "Betong",
    'emission_factors':
        {
            'product_id': 3,
            'A1': 12,
            'A2': 5,
            'A3': 6,
            'A4': 8,
            'C1': 1,
            'C2': 4,
            'C3': 3,
            'C4': 2,
            'D': 13,
            'A1A2A3': 0
        }
    }
]



if __name__ == '__main__':
    for user in users:
        add_userdata_to_db(user)

    for project in projects:
        post_project_to_db(project)
    
    for product in products:
        add_product_data(product)




# søppelbøtte

# def get_project_data_from_id(project_id):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('userdata.db')
#     conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
#     cur = conn.cursor()

#     # Fetch project details
#     cur.execute("""
#         SELECT * FROM Projects WHERE project_id = ?
#     """, (project_id,))
#     project_data = cur.fetchone()

#     # Check if the project exists
#     if project_data is None:
#         return None

#     # Fetch all products associated with this project
#     cur.execute("""
#         SELECT * FROM Products WHERE project_id = ?
#     """, (project_id,))
#     products = cur.fetchall()

#     # Convert project data and products into a dictionary
#     project_dict = dict(project_data)
#     project_dict['products'] = []

#     # Iterate over each product and fetch its emission factors
#     for product in products:
#         product_dict = dict(product)

#         # Fetch emission factors for this product
#         cur.execute("""
#             SELECT * FROM EmissionFactors WHERE material_id = ?
#         """, (product_dict['product_id'],))
#         emission_factors = cur.fetchone()
        
#         # Add the emission factors directly to the product dictionary if they exist
#         if emission_factors:
#             product_dict.update(dict(emission_factors))

#         # Append the product data to the project's products list
#         project_dict['products'].append(product_dict)

#     # Close connection
#     conn.close()

#     return project_dict