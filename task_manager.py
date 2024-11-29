from task_list import TaskList, JsonFileManager
from utils.input_utils import *
from utils.system_utils import clean_console
import os

option_input_message = 'Выберите действие (1 - Просмотреть задачи; 2 - Добавить задачу; 3 - Изменить задачу; 4 - Удалить задачу; 5 - Настройки; 6 - прервать выполнение программы): '
show_option_input_message = 'Какую задачу вы хотите увидеть? (1 - Все задачи; 2 - Задачи определенной категории; 3 - Конретную задачу; 4 - Вернуться в меню): '
delete_option_input_message = 'Какие задачи вы хотите удалить? (1 - Конкретную задачу; 2 - Все задачи определенной категории; 3 - Вернуться в меню): '
change_option_input_message = 'Что вы хотите изменить в задаче? (1 - Статус; 2 - Другие поля; 3 - Вернуться в меню): '
change_task_fields_message = 'Введите значения для полей задачи, которые хотите изменить (если не хотите менять какое поле, пропустите его): '
option_error_message = 'Такой опции не существует.'
setting_option_input_message = 'Выберите что хотите изменить (1 - директорию; 2 - тип сохраняемых данных): '

class TaskManager:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.file_manager = JsonFileManager(data_path)
        self.manager = TaskList(self.file_manager)
    
    def get_option(self) -> None:
        show_option = input(show_option_input_message)
        if show_option == '1':
            tasks = self.manager.get()
            for task in tasks:
                task.show()
        elif show_option == '2':
            category = input('Введите категорию: ')
            tasks = self.manager.get(category=category)
            for task in tasks:
                task.show()
        elif show_option == '3':
            task_id = input('Введите id задачи: ')
            tasks = self.manager.get(task_id=task_id)
            for task in tasks:
                task.show()
        elif show_option == '4':
            clean_console()
        else:
            clean_console()
            print(option_error_message)
            
    def add_option(self) -> None:
        data = task_input('Введите значение полей новой задачи', all_required=True)
        if data:
            self.manager.add(data)
            print('Задача успешно добавлена')
        else: 
            clean_console()
        
    
    def change_option(self) -> None:
        id = input('Введите id задачи, которую хотите изменить: ')
        change_option = input(change_option_input_message)
        if change_option == '1':
            status = input('Введите новый статус задачи: ')
            data = {'status': status}
            self.manager.change(id, data)
            print('Статус задачи успешно изменен')
        elif change_option == '2':
            data = task_input(change_task_fields_message)
            if data:
                self.manager.change(id, data)
                print('Поля задачи успешно изменены.')
        elif change_option == '3':
            clean_console()
        else:
            clean_console()
            print(option_error_message)
            
    def delete_option(self) -> None:
        delete_option = input(delete_option_input_message)
        if delete_option == '1':
            task_id = input('Введите id задачи: ')
            self.manager.delete(task_id=task_id)
            print('Задача успешно удалена')
        elif delete_option == '2':
            category = input('Введите категорию: ')
            self.manager.delete(category=category)
            print(f'Задачи категории "{category}" успешно удалены.')
        elif delete_option == '3':
            clean_console()
        else:
            clean_console()
            print(option_error_message)
            
    def settings_option(self) -> None:
        print(f'Текущая директория для хранения данных: {self.data_path}')
        print(f'Текущий тип сохраняемых дынных: {'json'}')
        
        setting_option = input(setting_option_input_message)
        if setting_option == '1':
            new_path = input('Введите путь до новой директории: ')
            all_data = self.file_manager.read()
            new_file_manager = JsonFileManager(new_path)
            new_file_manager.write(all_data)
            os.remove(self.data_path)
            self.file_manager = new_file_manager
            self.manager = TaskList(new_file_manager)
            self.data_path = new_path
        elif setting_option == '2':
            print('Смена типа в процессе разработки')
        else:
            print(option_error_message)
            
    def start(self) -> None:
        clean_console()
        print('Привет!')
        while True:
            option = input(option_input_message)
            clean_console()
            
            if option == '1':
                self.get_option()
            elif option == '2': 
                self.add_option()
            elif option == '3':
                self.change_option()
            elif option == '4':
                self.delete_option()
            elif option == '5':
                self.settings_option()
            elif option == '6':
                break
            else:
                clean_console()
                print(option_error_message)
        print('До новых встреч!')