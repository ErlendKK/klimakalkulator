import os
import sys
import json
from colorama import Fore, init

# Get the absolute path of the current directory and append the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from handle_db import add_user_to_db, add_project_to_db, add_product_to_db

init(autoreset=True)

def add_test_data_to_db(json_data):
    """Populates database with test-data"""
    for user in json_data['users']:
        add_user_to_db(user)

    for project in json_data['projects']:
        add_project_to_db(project)

    for product in json_data['products']:
        add_product_to_db(product)

if __name__ == '__main__':
    """Convert the JSON file into a dict.
    And pass it to add_test_data_to_db()
    """
    try:
        json_file_path = os.path.join(current_dir, 'test_data.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        add_test_data_to_db(json_data)
        
    except Exception as e:
        print(Fore.RED + f"test_db.py FAILED: {e}")
