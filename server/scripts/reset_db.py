import os
import create_db
from get_db_path import DATABASE
from colorama import Fore

def delete_database(db_file):
    """Delete the existing database file if it exists."""
    if os.path.exists(db_file):
        os.remove(db_file)
        print(Fore.GREEN+f"Deleted database SUCCEEDED for file: {db_file}")
    else:
        print(Fore.RED+f"Deleted database FAILED: No database found for file: {db_file}.")
    

def main():
    try:
        delete_database(DATABASE)
        create_db.main()
        
    except Exception as e:
        print(Fore.RED+f"delete_database FAILED: {e}")

if __name__ == '__main__':
    main()