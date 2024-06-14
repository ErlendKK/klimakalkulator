import os

def get_base_path():
    """Determines the base path for data files dynamically.
    Get the absolute path of the directory where the script is located
    Check if the current working directory ends with 'server'
    If the script is in 'scripts' directory, move one level up to 'server'
    Returns the path to the 'server' directory.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(os.getcwd()) == 'server':
        return os.getcwd()
    else:
        return os.path.dirname(script_dir)  
    
SERVER_DIR = get_base_path()
FILE_NAME = 'userdata.db'
DATABASE = os.path.join(SERVER_DIR, FILE_NAME)