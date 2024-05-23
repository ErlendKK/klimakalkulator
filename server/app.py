from flask import Flask, session, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from handle_db import (
    add_user_to_db, get_userdata_from_db, validate_and_return_user_data, 
    add_project_to_db, get_project_data_from_db, delete_project_data, update_project_data,
    add_product_to_db, delete_product_data, update_product_data, validate_product_for_update
)
from handle_ecoportal import fetch_emission_factors, fetch_productlist
import uuid
import os
import sys
import re


SERVER_URL = "http://localhost:5000"
VUE_DEV_SERVER = ["http://localhost:5173"]
VUE_STATIC_FOLDER = os.path.abspath('../frontend/dist')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # for profile pictures
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'user_data')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Setup App and sessions
app = Flask(__name__, static_folder=UPLOAD_FOLDER, template_folder=VUE_STATIC_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
app.secret_key = 'asdpoiJOIJpoj24985u9hjfs9u89H90h9H9HFOSJIASDJfsajf9o2j34r9ofj'

# Ensure HTTPS when using SameSite=None
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

# Setup for serving static Vue App in dev/built mode
is_frontend_built = 'built' in sys.argv
if is_frontend_built:
    CORS(app, supports_credentials=True) # Allow all origins
    print("Running with built frontend...")
else:
    CORS(app, supports_credentials=True, origins=VUE_DEV_SERVER)
    print("Running in development mode...")

# Base routing-function for built app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """Handles all incoming requests to the server. 
    Looks for the path in the directory VUE_STATIC_FOLDER, and serves the html if found. 
    Returns index-html for all non-existent routes.
    """
    if path != "" and os.path.exists(os.path.join(VUE_STATIC_FOLDER, path)):
        return send_from_directory(VUE_STATIC_FOLDER, path)
    return send_from_directory(VUE_STATIC_FOLDER, 'index.html')


################################################################
######## USERS API #############################################
################################################################


@app.route('/users/register', methods=['POST'])
def register_user():
    """Valid requests include name, email, password, and an optional image-file in form-format
    If photo is included, it is stored in UPLOAD_FOLDER under a generated 'photo_filename'
    Returns a json with properties status and data=(name, email, photo_filename, photo-url, and project_list)
    project_list is a nested lists of product-data.
    """
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    stay_logged_in = request.form['stayLoggedIn']
    submitted_data = {'name': name, 'email': email, 'password': password, 'stayLoggedIn': stay_logged_in}

    validation_result = validate_user_registration(submitted_data)
    print(validation_result['message'])
    if validation_result['status'] != 'success':
        return jsonify(validation_result), 401

    # Store photo if submitted
    photo = request.files['photo'] if 'photo' in request.files else None
    submitted_data['photo_filename'] = rename_and_store_photo(photo) \
        if photo is not None and validate_file(photo) else None

    # Post user data to db and return response-data to the frontend
    db_response = add_user_to_db(submitted_data)
    print(db_response['message'])

    if db_response['status'] == "success":
        updated_user_data = {k:v for k, v in db_response["user_data"].items() if k != 'password_hash'}
        establish_session(updated_user_data)
        return jsonify({"status": "success", "user_data": updated_user_data }), 200
    else:
        return jsonify(db_response), 401


def validate_user_registration(user_data):
    """Validates user registration data ensuring all required fields meet the criteria.
    Params: user_data: dict containing 'name', 'email', and 'password'.
    Returns: dict containing status and failure-message (in case of failure).
    
    - Name must not be empty and must contain at least one alphabetic character.
    - Email must be in a standard email format.
    - Password must be at least 8 characters long and include at least one digit and one letter.
    """
    name = user_data['name']
    email = user_data['email']
    password = user_data['password']

    # Validate name
    if not name:
        return {'status': 'failed', 'message': 'Navn mangler'}
    if not any(char.isalpha() for char in name):
        return {'status': 'failed', 'message': 'Navn har feil format'}
    
    # Validate email using regex (the part "(\.[a-zA-Z0-9-]+)*" handles sub-domains)
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]+$'
    if not re.match(email_pattern, email):
        return {'status': 'failed', 'message': 'Eposten har feil format'}
    
    # Validate password
    if len(password) < 8:
        return {'status': 'failed', 'message': 'Passordet er for kort'}
    if not (any(char.isdigit() for char in password) and any(char.isalpha() for char in password)):
        return {'status': 'failed', 'message': 'Passordet må inneholde både bokstaver og tall'}
    
    return {'status': 'success', 'message': f'User data has been validated for: {name}'}


def validate_file(file):
    # Validate format and filesize (5Mb)
    filename = file.filename
    file_format_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    file_size_allowed = file.content_length <= 5 * 1024 * 1024
    
    return file_format_allowed and file_size_allowed


def rename_and_store_photo(photo):
    try:
        original_filename = secure_filename(photo.filename)
        unique_id = uuid.uuid4().hex
        extension = original_filename.rsplit('.', 1)[1].lower()
        photo_filename = f"{unique_id}.{extension}"
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)
        return photo_filename
    
    except Exception as e:
        print(f"Failed to save photo: {e}")
        return None 


@app.route('/login', methods=['POST'])
def login_user():
    """Valid requests include email and password in json-format
    Validates email/password combination
    Starts a new session
    Returns name, email, photo_filename, project_list, and photo-url
    """
    login_data = request.get_json()
    user_data = validate_and_return_user_data(login_data) # returns (name, email, photo_filename, and project_list)
    print(user_data['message'])

    if user_data['status'] != 'success':
        return jsonify(user_data), 401 
    else:
        user_data['stayLoggedIn'] = login_data['stayLoggedIn']
        establish_session(user_data) 
        return jsonify(user_data), 200


def establish_session(user_data):
    session.clear()
    user_data['photo_url'] = get_photo_URL(user_data)
    session['user_id'] = user_data['user_id']
    session['project_ids'] = [project['project_id'] for project in user_data['projects']]
    session['stay_logged_in'] = user_data['stayLoggedIn']
    print(session)


@app.route('/logout', methods=['POST'])
def logout():
    print('logout called')
    session.pop('user_id', None)
    session['stay_logged_in'] = False
    session['project_ids'] = []
    return jsonify({"isLoggedIn": False}), 200


@app.route('/session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    print(f'check_session called for user_id: {user_id}')
    stay_logged_in = session.get('stay_logged_in')

    if user_id is None or not stay_logged_in:
        return jsonify({'status': 'failure', 'message': 'session not found'})
    
    user = get_userdata_from_db('user_id', user_id)
    if not user:
        return jsonify({'status': 'failure', 'message': 'user not found'}), 404
    
    user_data = {k:v for k, v in user.items() if k != 'password_hash'}
    user_data['projects'] = get_project_data_from_db(user_id)
    user_data['photo_url'] = get_photo_URL(user_data)
    return user_data, 200


def get_photo_URL(user_data):
    photo_filename = user_data['photo_filename']
    return f"{SERVER_URL}/user_data/{photo_filename}" if photo_filename else None


################################################################
########## PROJECTS API ########################################
################################################################


@app.route('/projects/register', methods=['POST'])
def register_project():
    """Registers a new project. Requires a logged-in user.
    Params: data: dict of project data
    If successful, returns a jsonified dict of the input data
    with added properties for project_id, status and message
    """
    project_data = request.get_json()
    print(project_data)

    # Check if user is in session. If not, return status: failed and error-message
    authentication_response = authenticate_user(project_data)
    if authentication_response['status'] != 'success':
        return jsonify(authentication_response), 401
    
    # Check if input data is valid. If not, return status: failed and error-message
    validation_response = validate_project_data(project_data)
    print(validation_response['message'])
    if validation_response['status'] != 'success':
        return jsonify(validation_response), 400
    
    # Add prosject to db. Upon error, return status: failed and error-message
    db_response = add_project_to_db(project_data)
    if db_response['status'] == "success":
        session['project_ids'].append(db_response['project_id'])
        session.modified = True
        return jsonify(db_response), 200
    else:
        return jsonify({"status": "failed", "message": "Registreringen mislyktes"}), 400


def authenticate_user(data):
    """Validate that the user is logged in and correct"""
    if not data['user_id']:
        return {"status": "failed", "message": "En feil har oppstått"}
    if data['user_id'] != session['user_id']:
        message = 'Prosjekteier er ikke logget inn, eller mangler rettigheter til å oppdatere prosjektet'
        return {'status': 'failed', 'message': message}
    
    return {'status': 'success'}


def validate_project_data(data):
    """Validates the format, datatype and length of the mandatory fields for project registration.
    Props: data: dict of project_data passed as body in http-request
    Returns: dict containing validation-status and message
    """
    
    # Field validations with pattern matching and length checks
    patterns = {
        'name': r"^.*$",
        'address': r"^.*$",
        'bta': r"^\d+$",
        'analyseperiode': r"^\d+$",
        'prosjektstart': r"^\d{4}$"
    }

    for key, pattern in patterns.items():
        value = data.get(key) 
        if isinstance(value, int):
            value = str(value)
            
        if not value or not re.match(pattern, value) or len(value) > 100:
            message = f"{key.capitalize()} mangler eller er ugyldig"
            if len(value) > 100:
                message = f"{key.capitalize()} overstiger 100 tegn"
            return {"status": "failed", "message": message}

    return {"status": "success", "message": f"Prosjektdata er validert for {data['name']}"}
    

@app.route('/projects/update', methods=['PUT'])
def update_project():
    project_data = request.get_json()
    print(project_data)

    # Check if user is in session. If not, return status: failed and error-message
    authentication_response = authenticate_user(project_data)
    if authentication_response['status'] != 'success':
        return jsonify(authentication_response), 401
    
    # Check if input data is valid. If not, return status: failed and error-message
    validation_response = validate_project_data(project_data)
    print(validation_response['message'])
    if validation_response['status'] != 'success':
        return jsonify(validation_response), 400

    # Add prosject to db. Upon error, return status: failed and error-message
    db_response = update_project_data(project_data)
    if db_response['status'] == 'success':
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400  


@app.route('/projects/delete/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    # Convert id to string as expected by the called functions
    try:
        project_id = int(project_id)
    except ValueError:
        return jsonify({'status': 'failed', 'message': 'Ugyldig prosjekt ID'}), 400
    
    # Authenticate user by verifying that the project is in session
    if project_id not in session['project_ids']:
        message = 'Prosjekteier er ikke logget inn, eller mangler rettigheter til å slette prosjektet'
        print(message)
        return jsonify({'status': 'failed', 'message': message}), 401
    
    # Remove the project from db and session, return status and message.
    db_response = delete_project_data(project_id)
    if db_response['status'] == 'success':
        session['project_ids'].remove(project_id)
        session.modified = True 
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400   


################################################################
########## PRODUCTS API ########################################
################################################################


@app.route('/products/add', methods=['POST'])
def add_product_to_project():
    """Takes as input a json containing 'project_id' and product data from the ecoportal product-list
    Returns a json containing "emission_factors" (dict of floats) and unit (string)
    """
    data = request.get_json()
    print(data)

    if data['project_id'] not in session['project_ids']:
        return jsonify({'status': 'failed', 'message': 'Prosjekeieren er ikke logget inn'}), 401

    added_product = add_product_to_db(data)
    added_product['emission_factors'] = data.get('emission_factors', {})
    added_product['unit']  = data.get('unit', None)

    if added_product['status'] == 'success':
        return jsonify(added_product), 200
    else:
        return jsonify(added_product), 400  
    

@app.route('/products/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    validation_result = validate_product_for_update(product_id)
    if validation_result['status'] != 'success':
        print(validation_result['message'])

        code = validation_result['code']
        del validation_result['code']
        return jsonify(validation_result), code

    db_response = delete_product_data(product_id)

    if db_response['status'] == 'success':
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400   


@app.route('/products/update', methods=['PUT'])
def update_product():
    product_data = request.get_json()
    print(product_data)

    validation_result = validate_product_for_update(product_data['product_id'])
    if validation_result['status'] != 'success':
        print(validation_result['message'])

        code = validation_result['code']
        del validation_result['code']
        return jsonify(validation_result), code
    
    db_response = update_product_data(product_data)

    if db_response['status'] == 'success':
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400   


@app.route('/products/emission-data/<uuid>', methods=['GET'])
def ecoportal_properties(uuid):
    """Takes an ecoportal uuid as input
    Fetches emission factors and reference-data from ecoportal
    Returns a json containing "emission_factors" (dict of floats) and "unit" (string)
    """
    print('uuid: ', uuid)
    eco_portal_response = fetch_emission_factors(uuid)

    if eco_portal_response['status'] == 'success':
        return jsonify(eco_portal_response), 200
    else:
        return jsonify(eco_portal_response), 400
    

@app.route('/products/list', methods=['GET'])
def get_productlist():
    eco_portal_response = fetch_productlist()
    print(eco_portal_response['message'])

    if eco_portal_response['status'] == 'success':
        return jsonify(eco_portal_response), 200
    else:
        return jsonify(eco_portal_response), 400        


if __name__ == '__main__':
    app.run()