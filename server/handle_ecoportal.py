import requests
import json
import os
from colorama import Fore, init
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), 'db_credentials.env')
load_dotenv(dotenv_path=env_path)
init(autoreset=True)

ECOPORTAL_API_TOKEN  = os.getenv('ECOPORTAL_API_TOKEN')

# ECOPORTAL_API_TOKEN = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJFcmxlbmQiLCJpc3MiOiJFQ09QT1JUQUwiLCJhdWQiOiJhbnkiLCJ2ZXIiOiI3LjkuNyIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCx3cml0ZTo2ODgiLCJzdG9jazpyZWFkLGV4cG9ydDoyIiwic3RvY2s6cmVhZCxleHBvcnQ6MSJdLCJyb2xlcyI6W10sImlhdCI6MTcxMjU3NTA4NSwiZXhwIjoxNzIwNDU5MDg1LCJlbWFpbCI6ImVybGVuZGtAbGl2ZS5jb20iLCJ0aXRsZSI6ImhoIiwiZmlyc3ROYW1lIjoiRXJsZW5kICIsImxhc3ROYW1lIjoiS3ZpdHJ1ZCIsImdlbmVyYXRlTmV3VG9rZW5zIjpmYWxzZSwiam9iUG9zaXRpb24iOiJFbmdpbmVlciIsImFkZHJlc3MiOnsiY2l0eSI6IlN0YXZhbmdlciIsInppcENvZGUiOiI0MDE2IiwiY291bnRyeSI6Ik5PIiwic3RyZWV0IjoiIn0sIm9yZ2FuaXphdGlvbiI6e30sInVzZXJHcm91cHMiOlt7InVzZXJHcm91cE5hbWUiOiJyZWdpc3RlcmVkX3VzZXJzIiwidXNlckdyb3VwT3JnYW5pemF0aW9uTmFtZSI6IkRlZmF1bHQgT3JnYW5pemF0aW9uIn1dLCJhZG1pbmlzdHJhdGVkT3JnYW5pemF0aW9uc05hbWVzIjoiIiwicGhvbmUiOiI5NzExMTg0MSIsImRzcHVycG9zZSI6IkFuIExDQSB3ZWJhcHAgIiwic2VjdG9yIjoiIiwiaW5zdGl0dXRpb24iOiJWZW5pIn0.ru36AZheBwYK8_N3d9YNBYfLIcEWMtmOV0hNs7a_sgGPheZL9DVrjJXdotypysodIJGTvMd-QqEALyCVOms3ntABTDYB4NCBqydJLTX1H8R8Gu0AvNIldtRxhhrEfEpjzLnv0itddlMuRqYVxB46EAP3eNft4NXqvpyHdJS73Pk'
ECOPORTAL_BASE_URL = 'https://epdnorway.lca-data.com/resource/processes'

def fetch_productlist():
    """retrieves a list of products from the EcoPortal API, 
    filters out outdated and non-building components, and appends URLs from a local JSON file. 
    Returns the product list with a status message indicating success or failure.
    """
    query_string  = '?search=true&validUntil=2024&format=JSON'
    headers = {'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'}
    
    try:
        response = requests.get(f'{ECOPORTAL_BASE_URL}{query_string}', headers=headers)
        response.raise_for_status()
        data = response.json()
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
            # Only include non-electrical building components
            for item in items
            if "Bygg" in item.get("classific", "") and 
               "Elektroniske og elektriske komponenter og produkter" not in item.get("classific", "") and
               "Elektriske kabler"  not in item.get("classific", "")
        ]

        uuid_list = [product['uuid'] for product in ecoportal_productlist]
        epd_urls = load_epd_urls('epd_urls.json')
        url_uuid_dict = extract_epd_url(uuid_list, epd_urls)

        for product in ecoportal_productlist:
            uuid = product['uuid']
            product['epd_url'] = url_uuid_dict[uuid]

        returnDict = {'status': 'success', 'message': 'fetch_productlist SUCCESSFUL', 'data': ecoportal_productlist}
        return returnDict

    except requests.exceptions.HTTPError as e:
        print(Fore.RED+f"fetch_productlist FAILED to fetch productlist from EcoPortal: {e}")
        return {"status": 'failed', 'message': f"Fetching productlist failed"}
    
    except Exception as e:
        print(Fore.RED+f"fetch_productlist FAILED to decode JSON: {e}")
        return {"status": 'failed', 'message': f"Decoding JSON failed"}


def fetch_emission_factors(uuid):
    """Retrieves emission factor data for a specific product from the EcoPortal API. 
    Processes the retrieved data to extract relevant emission factors and unit information
    Returns this information with a status message indicating success or failure.
    """
    query_string = '?format=JSON&view=extended'
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    path = f'{ECOPORTAL_BASE_URL}/{uuid}{query_string}'
    response = requests.get(path, headers=headers)

    if response.status_code != 200:
        print(Fore.RED+"fetch_emission_factors FAILED to fetch data, status code:", response.status_code)
        return {'status': 'failed', 'message': 'API call failed'}
    
    try:
        lca_data = response.json()
        emission_factors = extract_emission_factors(lca_data)
        unit_data = extract_unit_data(lca_data)

        return_values = {
            'emission_factors': emission_factors,
            'unit': unit_data.get('referenceUnit', None),
            'status': 'success'
        }

        return return_values
    
    except ValueError as e:
        print(Fore.RED+f"fetch_emission_factors FAILED: {e}")
        return {'status': 'failed', 'message': 'Invalid JSON data'}


def extract_epd_url(lca_data):
    """Extracts the EPD URL from the input product data. 
    Returns the URL if found. Otherwise; returns an empty string
    """
    try:
        resource_urls = lca_data['modellingAndValidation']['dataSourcesTreatmentAndRepresentativeness']['other']['anies'][0]['value']['resourceURLs']
        return resource_urls[0]
    
    except Exception as e:
        print(Fore.RED+f"fetch_emission_factors FAILED. EPD Document MISSING! {e}")
        return ''


def extract_emission_factors(data):
    """Extracts GWP-total emission factors from an LCIA datatable.
    Loops through the LCIAResult array and looks for "Global Warming Potential - total (GWP-total)"
    IF not found, this means the EPD is simple => look for just "Global Warming Potential"
    If found: Loops through the entries to extract emission factors and returns the result
    """
    print('extract_emission_factors called')
    LIFECYCLE_PHASES = ['A1', 'A2', 'A3', 'A4', 'C1', 'C2', 'C3', 'C4', 'D']
    emission_factors = {}
    
    for result in data["LCIAResults"]["LCIAResult"]:
        # Access the shortDescription correctly
        short_descriptions = result["referenceToLCIAMethodDataSet"]["shortDescription"]
        
        if any(sd["value"] == "Global Warming Potential - total (GWP-total)" for sd in short_descriptions):
            entries = result["other"]["anies"]
            for entry in entries:
                if "module" in entry:
                    emission_factors[entry["module"]] = floatify(entry["value"])

        elif any(sd["value"] == "Global warming potential (GWP)" for sd in short_descriptions):
            entries = result["other"]["anies"]
            for entry in entries:
                if "module" in entry:
                    emission_factors[entry["module"]] = floatify(entry["value"])

    # Check for missing lifecycle phases and initialize them with 0 if absent
    for phase in LIFECYCLE_PHASES:
        if phase not in emission_factors:
            emission_factors[phase] = 0

    emission_factors['A1A2A3'] = emission_factors['A1-A3'] if 'A1-A3' in emission_factors else 0
    return emission_factors


def floatify(stringified_float):
    """Convert number, formated as string, into a float"""
    try:
        floatified_float = float(stringified_float)
        return floatified_float
    except Exception as e:
        print(Fore.RED+f'floatify FAILED to floatify {stringified_float}: {e}')
        return 0
        

def extract_unit_data(data):
    """Extracts the reference unit of the input data-dict and calls normalize_units."""
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
    """Converts '1000 kg' to '1 tonn'
    Translates 'Stück' to 'stykk'
    """
    if (unit_data['referenceUnit'].lower() == 'kg' and unit_data['resultingflowAmount'] == 1000):
        unit_data['referenceUnit'] = 'tonn'
        unit_data['resultingflowAmount'] = 1

    if unit_data['referenceUnit'].lower() == 'stück':
        unit_data['referenceUnit'] = 'stykk'


def load_epd_urls(filename):
    """Load the EPD URL data from a JSON file.
    """
    print('load_epd_urls called')
    try:
        base_path = get_server_path()
        file_path = os.path.join(base_path, filename)
        print('load_epd_urls, file_path:', file_path)
        
        with open(file_path, 'r') as file:
            epd_urls = json.load(file)
        return epd_urls
    
    except FileNotFoundError:
        print(Fore.RED+"The file was not found.")
        return {}
    
    except json.JSONDecodeError:
        print(Fore.RED+"Failed to decode JSON.")
        return {}


def get_server_path():
    """Determines the base path for data files dynamically.
    Gets the directory where the script is located
    Defines the path to the 'server' directory relative to the script
    Checks if running from within 'server' directory to avoid duplication in path
    """
    server_dir = os.path.dirname(__file__)
   
    if os.getcwd().endswith('server'):
        server_dir = os.getcwd()
    return server_dir 


def extract_epd_url(uuids, epd_urls):
    """Fetch URLs for a list of UUIDs using the EPD URL data.
    """
    url_data = {}

    for uuid in uuids:
        url = epd_urls.get(uuid)
        if url:
            url_data[uuid] = url
        else:
            url_data[uuid] = ""
    return url_data

