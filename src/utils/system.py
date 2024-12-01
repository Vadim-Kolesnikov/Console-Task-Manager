import os
import csv
import json




def clean_console(message_after_clean: str = '') -> None:
    '''Очищает консоль'''

    os.system('cls' if os.name == 'nt' else 'clear')
    print(message_after_clean)
    

def search_data_path(file_type: str = '.json') -> list[str]:
    '''
    Ищет в текущей директории файлы
    с расширением .json / .csv
    '''

    listdir = os.listdir()
    path_list = []
    for path in listdir:
        if path.endswith(file_type):
            path_list.append(path)
    return path_list


def find_file_info() -> None | tuple[str]:
    '''
    Проверяет файловую структуру на корректность
    и, если все правильно возвращает путь до .json / .csv файла.
    если файла нет, возвращется путь по умолчанию.
    корректной считается структура в которой существует
    только один файл json или csv или вообще нет файлов с таким расширением
    '''

    json_data_path_list = search_data_path('.json')
    csv_data_path_list = search_data_path('.csv')

    file_path = None

    if len(json_data_path_list) > 0 and len(csv_data_path_list) > 0:
        print('В каталоге файла должен рапологаться только один файл .json или один файл .csv')
    elif len(json_data_path_list) > 0:
        if len(json_data_path_list) > 1:
            print('В каталоге файла должен рапологаться только один файл .json')
            return None
        else:
            file_path = json_data_path_list[0]
    elif len(csv_data_path_list) > 0:
        if len(csv_data_path_list) > 1:
            print('В каталоге файла должен рапологаться только один файл .csv')
            return None
        else:
            file_path = csv_data_path_list[0]      
    else:
        file_path = 'data.json'

    separated_data_path = file_path.split('.')

    if len(separated_data_path) == 2:
        file_name = separated_data_path[0]
        file_type = separated_data_path[1]
    else:
        print('Некорректное название файла (пример названия: data.json)')
        return None
    
    return file_name, file_type


class CsvFileManager:
    '''Вспомогательный класс для работы с .csv файлами'''

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> list[dict]:
        '''
        Метод читает все данный из файл.
        Если он пуст или его не существует, 
        возвращается пустой спиоск
        '''

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', newline="") as file:
                reader = csv.DictReader(file)
                data = []
                for row in reader:
                    data.append(row)
            return data
        return []

    def write(self, data: list[dict]) -> None:
        '''
        Метод записывает переданные данные в файл.
        Если файла нет, метод его создает
        '''

        columns = list(data[0].keys())
        with open(self.file_path, 'w', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
        

class JsonFileManager:
    '''Вспомогательный клас для работы с .json файлами'''

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> list[dict]:
        '''
        Метод читает все данный из файл.
        Если он пуст или его не существует, 
        возвращается пустой спиоск
        '''

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        return []

    def write(self, data: list[dict]) -> None:
        '''
        Метод записывает переданные данные в файл.
        Если файла нет, метод его создает
        '''

        with open(self.file_path, "w") as file:
            json.dump(data, file)