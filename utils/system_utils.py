import os

# функция для очистки консоли
def clean_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    

# функция ищет в текущей директории файлы
# с расширением .json 
def search_data_path() -> str:
    listdir = os.listdir()
    data_path = None
    for path in listdir:
        if path.endswith('.json'):
            return path
    return 'data.json'
    
    