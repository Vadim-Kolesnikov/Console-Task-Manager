import os

def clean_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    

def search_data_path():
    listdir = os.listdir()
    data_path = None
    for path in listdir:
        if path.endswith('.json'):
            return path
    return 'data.json'
    
    