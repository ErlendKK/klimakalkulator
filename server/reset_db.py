import os
import create_db

def delete_database(db_file):
    """Delete the existing database file if it exists."""
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted database file: {db_file}")
    else:
        print(f"No database file found at: {db_file}, nothing to delete.")

def main():
    database = 'userdata.db'
    delete_database(database)
    create_db.main()  

if __name__ == '__main__':
    main()