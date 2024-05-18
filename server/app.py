from flask import Flask, session, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from handle_db import add_userdata_to_db, validate_and_return_user_data, get_userdata_from_db, add_product_data, delete_product_data, update_product_data, get_project_data, post_project_to_db, delete_project_data, update_project_data
import requests
import uuid
import os
from werkzeug.utils import secure_filename

SERVER_URL = "http://localhost:5000"
ECOPORTAL_API_TOKEN = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJFcmxlbmQiLCJpc3MiOiJFQ09QT1JUQUwiLCJhdWQiOiJhbnkiLCJ2ZXIiOiI3LjkuNyIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCx3cml0ZTo2ODgiLCJzdG9jazpyZWFkLGV4cG9ydDoyIiwic3RvY2s6cmVhZCxleHBvcnQ6MSJdLCJyb2xlcyI6W10sImlhdCI6MTcxMjU3NTA4NSwiZXhwIjoxNzIwNDU5MDg1LCJlbWFpbCI6ImVybGVuZGtAbGl2ZS5jb20iLCJ0aXRsZSI6ImhoIiwiZmlyc3ROYW1lIjoiRXJsZW5kICIsImxhc3ROYW1lIjoiS3ZpdHJ1ZCIsImdlbmVyYXRlTmV3VG9rZW5zIjpmYWxzZSwiam9iUG9zaXRpb24iOiJFbmdpbmVlciIsImFkZHJlc3MiOnsiY2l0eSI6IlN0YXZhbmdlciIsInppcENvZGUiOiI0MDE2IiwiY291bnRyeSI6Ik5PIiwic3RyZWV0IjoiIn0sIm9yZ2FuaXphdGlvbiI6e30sInVzZXJHcm91cHMiOlt7InVzZXJHcm91cE5hbWUiOiJyZWdpc3RlcmVkX3VzZXJzIiwidXNlckdyb3VwT3JnYW5pemF0aW9uTmFtZSI6IkRlZmF1bHQgT3JnYW5pemF0aW9uIn1dLCJhZG1pbmlzdHJhdGVkT3JnYW5pemF0aW9uc05hbWVzIjoiIiwicGhvbmUiOiI5NzExMTg0MSIsImRzcHVycG9zZSI6IkFuIExDQSB3ZWJhcHAgIiwic2VjdG9yIjoiIiwiaW5zdGl0dXRpb24iOiJWZW5pIn0.ru36AZheBwYK8_N3d9YNBYfLIcEWMtmOV0hNs7a_sgGPheZL9DVrjJXdotypysodIJGTvMd-QqEALyCVOms3ntABTDYB4NCBqydJLTX1H8R8Gu0AvNIldtRxhhrEfEpjzLnv0itddlMuRqYVxB46EAP3eNft4NXqvpyHdJS73Pk'
ECOPORTAL_BASE_URL = 'https://epdnorway.lca-data.com/resource/processes'

# gets current directory and sets UPLOAD_FOLDER = cd/profilephotos
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'user_data')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app = Flask(__name__, static_folder=UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# login_manager = LoginManager()
# login_manager.init_app(app)

# enable communication with the frontend server
development_origins = ["http://localhost:5173"]
production_origins = ["https://my-production-frontend.com"]
allowed_origins = development_origins if app.debug else production_origins

CORS(app, supports_credentials=True, origins=allowed_origins) 

uuid_list = [
  "94506cde-817c-4307-bef0-4a317b894e95",
  "19d94e69-362b-48b0-8130-71c9b7a43ad6",
  "58871b96-bcdf-4438-b82f-d100c1df1fe5",
  "982ea073-82cb-4515-aa4f-b2f7381105af",
  "5100c688-3a97-41b7-9223-d58916b04870",
  "5ace36b6-9f29-41a0-b4d6-b7fc6ba3f8ff",
  "f7283e72-d54f-4637-a1a8-368362a63f13"
]
QUERY_STRING = '?format=JSON&view=extended'
PATH = 'https://epdnorway.lca-data.com/resource/processes/a1db2cb9-fe80-4e27-85a5-8c574f6c3003?format=JSON&view=extended'



@app.route('/projects/update', methods=['PUT'])
def update_project():
    project_data = request.get_json()
    if project_data['user_id'] != session['user_id']:
        return jsonify({'status': 'failed', 'message': 'Prosjekeieren er ikke logget inn'})
    
    db_response = update_project_data(project_data)

    if db_response['status'] == 'success':
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400  
    

@app.route('/projects/delete/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    print(f'delete_project called for {project_id}')
    db_response = delete_project_data(project_id)

    if db_response['status'] == 'success':
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400   


@app.route('/products/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    db_response = delete_product_data(product_id)

    if db_response['status'] == 'success':
        return jsonify(db_response), 200
    else:
        return jsonify(db_response), 400   

@app.route('/products/update', methods=['PUT'])
def update_product():
    product_data = request.get_json()
    print(product_data)
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
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    path = f'{ECOPORTAL_BASE_URL}/{uuid}{QUERY_STRING}'
    response = requests.get(path, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch data, status code:", response.status_code)
        return jsonify({'status': 'failed', 'message': 'API call failed'})
    
    try:
        lca_data = response.json()
        emission_factors = extract_emission_factors(lca_data)
        unit_data = extract_unit_data(lca_data)

        return_values = {
            'emission_factors': emission_factors,
            'unit': unit_data.get('referenceUnit', None),
            'status': 'success'
        }
        print(return_values)

        return jsonify(return_values)
    
    except ValueError as e:
        print(f"{e}")
        return jsonify({'status': 'failed', 'message': 'Invalid JSON data'})

@app.route('/products/add', methods=['POST'])
def add_product_to_project():
    """Takes as input a json containing 'project_id' and product data from the ecoportal product-list
    Returns a json containing "emission_factors" (dict of floats) and unit (string)
    """
    data = request.get_json()
    print(data)
    added_product = add_product_data(data)
    added_product['emission_factors'] = data.get('emission_factors', {})
    added_product['unit']  = data.get('unit', None)

    if added_product['status'] == 'success':
        return jsonify(added_product), 200
    else:
        return jsonify(added_product), 400  

def extract_emission_factors(data):
    """Extracts GWP-total emission factors from an LCIA datatable.
    Loops through the LCIAResult array and looks for "Global Warming Potential - total (GWP-total)"
    IF not found, this means the EPD is simple => look for just "Global Warming Potential"
    When found: Loops through the anies entries to extract emission factors
    Map the module to its value and returns a dict of modules
    """
    LIFECYCLE_PHASES = ['A1', 'A2', 'A3', 'A4', 'C1', 'C2', 'C3', 'C4', 'D']
    emission_factors = {}
    
    for result in data["LCIAResults"]["LCIAResult"]:
        # Access the shortDescription correctly
        short_descriptions = result["referenceToLCIAMethodDataSet"]["shortDescription"]
        
        if any(sd["value"] == "Global Warming Potential - total (GWP-total)" for sd in short_descriptions):
            entries = result["other"]["anies"]
            for entry in entries:
                if "module" in entry:
                    emission_factors[entry["module"]] = float(entry["value"])

        elif any(sd["value"] == "Global warming potential (GWP)" for sd in short_descriptions):
            entries = result["other"]["anies"]
            for entry in entries:
                if "module" in entry:
                    emission_factors[entry["module"]] = float(entry["value"])

    # Check for missing lifecycle phases and initialize them with 0 if absent
    for phase in LIFECYCLE_PHASES:
        if phase not in emission_factors:
            emission_factors[phase] = 0

    emission_factors['A1A2A3'] = emission_factors['A1-A3'] if 'A1-A3' in emission_factors else 0
    return emission_factors

def extract_unit_data(data):
    """Extract the declared/reference unit and normalize units."""
    unit_data = {
        'resultingflowAmount': None,
        'referenceUnit': None
    }

    exchanges = data.get("exchanges", {}).get("exchange", [])
    # Loop through each exchange in the list
    for exchange in exchanges:
        if "referenceFlow" not in exchange or 'resultingflowAmount' not in exchange:
            continue
        unit_data['resultingflowAmount'] = exchange['resultingflowAmount']

        # Loop through the "flowProperties" to find the "referenceUnit"
        for flow_prop in exchange.get("flowProperties", []):
            if 'referenceFlowProperty' not in flow_prop:
                continue
            unit_data['referenceUnit'] = flow_prop.get("referenceUnit", None)
            
            # If unit data is found, normalize and return it
            if all(value is not None for value in unit_data.values()):
                normalize_units(unit_data)
                return unit_data

    return unit_data

def normalize_units(unit_data):
    # Convert '1000 kg' to '1 tonn'
    # And translate 'Stück' to 'stykk'
    if (unit_data['referenceUnit'].lower() == 'kg' and unit_data['resultingflowAmount'] == 1000):
        unit_data['referenceUnit'] = 'tonn'
        unit_data['resultingflowAmount'] = 1
    if unit_data['referenceUnit'].lower() == 'stück':
        unit_data['referenceUnit'] = 'stykk'

def fetch_emission_factor_from_ecoportal(uuid):
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    response = requests.get(f'{ECOPORTAL_BASE_URL}{uuid}?format=JSON', headers=headers)

    if response.status_code != 200:
        print("Failed to fetch data")
        return []
    
    try:
        lca_data = response.json()
        emission_factors = extract_emission_factors(lca_data)
        return emission_factors
    
    except ValueError:
        print("Failed to decode JSON")
        return []   

@app.route('/products/full-productlist', methods=['GET'])
def get_full_productlist():
    QUERY_STRING = '?search=true&validUntil=2024&format=JSON'

    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    response = requests.get(f'{ECOPORTAL_BASE_URL}{QUERY_STRING}', headers=headers)

    if not response.status_code == 200:
        print("Failed to fetch data")
        return jsonify({"status": 'failed', 'message': "Failed to fetch data"}), response.status_code
    
    data = response.json()  # Parse the JSON response
    try:
        items = data.get('data', []) 

        ecoportal_productlist = [
            {
                "uuid": item.get("uuid", "uuid missing"),
                "owner": item.get("owner", "owner missing"),
                "name": item.get("name", "name missing"),
                "regNo": item.get("regNo", "regNo missing"),
                "validUntil": item.get("validUntil", "validUntil missing"),
                "classific": item.get("classific", "classific missing").replace("Bygg / ", "")
            }
            for item in items
            if "Bygg" in item.get("classific", "")
        ]       

        return jsonify(ecoportal_productlist)
        # return jsonify(items)
    except ValueError:
        print("Decoding JSON has failed")
        return jsonify({"status": 'failed', 'message': "Decoding JSON has failed"}), 500

@app.route('/users', methods=['POST'])
def register_user():
    """Valid requests include name, email, password, and an optional image-file in form-format
    If photo is included, it is stored in UPLOAD_FOLDER under a generated 'photo_filename'
    Returns json (name, email, photo_filename, photo-url, and a project_list (which includes nested lists of product-data), 
    """
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    submitted_data = {'name': name, 'email': email, 'password': password}
    for key, value in submitted_data.items():
        print(key, value)

    if not validate_registration(submitted_data):
        return jsonify({"status": "failed", "message": "valideringen misslyktes"}), 401

    # Store photo if submitted
    photo = request.files['photo'] if 'photo' in request.files else None
    submitted_data['photo_filename'] = rename_and_store_photo(photo) \
        if photo is not None and validate_file(photo) else None

    # Post user data to db and return response-data to the frontend
    db_response = add_userdata_to_db(submitted_data)
    updated_user_data = {k:v for k, v in db_response.items() if k != 'password_hash'}
    
    if db_response['status'] == "success":
        return jsonify({"status": "success", "user_data": updated_user_data }), 200
    else:
        return jsonify(db_response), 401


def validate_file(file):
    filename = file.filename
    # Validate format
    file_format_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    # Validate filesize (5Mb)
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

    if user_data['status'] != 'success':
        print(user_data['message'])
        return jsonify(user_data), 401  

    session.clear()
    user_data['photo_url'] = get_photo_URL(user_data)
    session['user_id'] = user_data['user_id']
    session['project_ids'] = [project['project_id'] for project in user_data['projects']]
    session['stay_logged_in'] = login_data['stayLoggedIn']

    return jsonify(user_data), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session['stay_logged_in'] = False
    session['project_ids'] = []
    return jsonify({"isLoggedIn": False}), 200


@app.route('/session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    stay_logged_in = session.get('stay_logged_in')

    if user_id is None or not stay_logged_in:
        return jsonify({'status': 'failure', 'message': 'session not found'})
    
    user = get_userdata_from_db('user_id', user_id)
    if not user:
        return jsonify({'status': 'failure', 'message': 'user not found'}), 404
    
    user_data = {k:v for k, v in user.items() if k != 'password_hash'}
    user_data['projects'] = get_project_data(user_id)
    user_data['photo_url'] = get_photo_URL(user_data)
    return user_data, 200

def get_photo_URL(user_data):
    photo_filename = user_data['photo_filename']
    return f"{SERVER_URL}/user_data/{photo_filename}" if photo_filename else None


@app.route('/register_project', methods=['POST'])
def register_project():
    data = request.get_json()
    user_id = data['user_id']

    if user_id is None:
        return jsonify({"status": "failed", "message": "No user logged in"}), 401
    
    db_response = post_project_to_db(data)

    if validate_registration(data) and db_response['status'] == "success":
        print(db_response)
        return jsonify(db_response), 200
    else:
        return jsonify({"status": "failed", "message": "Invalid user"}), 401


@app.route('/get_project', methods=['GET'])
def get_project():
    project_id = request.args.get('project_id', type=int)
    if not project_id:
        return jsonify({"status": "failure", "message": "Project ID is required"}), 400

    project_data = get_project_data(project_id)
    if project_data is None:
        return jsonify({"status": "failure", "message": "Project not found"}), 404

    return jsonify(project_data)



# ------------------------------
# Production/Test functions below:
# ------------------------------



@app.route('/api/data', methods=['GET'])
def get_data():
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    response = requests.get(f'{PATH}', headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()

            # Filtrer data basert på "classific" som inneholder ordet "Bygg"
            print("Data fetched successfully:")
            emission_factors = extract_emission_factors(data)
            print(emission_factors)
            return jsonify(data)
        
        except ValueError:  # Catch JSON decoding errors
            print("Decoding JSON has failed")
            return jsonify({"status": "failed", "message": "Decoding JSON has failed"}), 500
    else:
        print("Failed to fetch data")
        return jsonify({"status": "failed", "message": response.status_code}), response.status_code





# TODO: implement logic with werkzeug.security password_hashes
def validate_registration(user_data):
    return True

def validate_login(name, password):
    """Checks if name-password combination is valid."""
    return True





if __name__ == '__main__':
    app.run()