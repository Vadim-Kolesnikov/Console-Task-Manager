from task_list import TaskList, show_tasks
from utils.system import JsonFileManager, CsvFileManager, clean_console
from utils.input import *
from settings import *
import os
import random as rd



# основной класс программы, предоставлящий интерфейс
# для взаимодействия пользователя с задачами
class TaskManager:
    def __init__(self, file_name: str, file_type: str) -> None:
        self.file_name = file_name
        self.file_type = file_type
        if file_type == 'csv':
            self.file_manager = CsvFileManager(file_name + '.' + file_type)
        else:
            self.file_manager = JsonFileManager(file_name + '.' + file_type)
        self.task_list = TaskList(self.file_manager)

    @property
    def file_path(self) -> str:
        return self.file_name + '.' + self.file_type
    
    def gen_tasks(self) -> None:
        tasks = []
        for i in range(0, len(task_names)):
            task = {}
            task['id'] = str(i)
            task["title"] = task_names[i]
            task["description"] = task_descriptions[i]
            task["category"] = task_categories[i]
            task["due_date"] = '22.04.2025'
            task["priority"] = rd.randint(0, len(priority_choices) - 1)
            task["status"] = rd.randint(0, len(status_choices) - 1)
            tasks.append(task)
        self.file_manager.write(tasks)
        print('Генерация прошлла успешно')
         
        
    
    # опция получения задачи/задач
    def get_option(self) -> None:
        show_option = input(show_option_input_message)
        if show_option == '1':
            tasks = self.task_list.get()
            clean_console()
            show_tasks(tasks)
        elif show_option == '2':
            category = input('Введите категорию: ')
            tasks = self.task_list.get(category=category)
            clean_console()
            show_tasks(tasks, message=f'Категория "{category}"')
        elif show_option == '3':
            task_id = id_validate_input('Введите id задачи: ')
            tasks = self.task_list.get(task_id=task_id)
            clean_console()
            show_tasks(tasks, message='')
        elif show_option == '4':
            clean_console()
        else:
            clean_console()
            print(option_error_message)
    
    # опция добавления задачи
    def add_option(self) -> None:
        data = task_input('Введите значение полей новой задачи', all_required=True)
        if data:
            self.task_list.add(data)
            clean_console('Задача успешно добавлена')
        else: 
            clean_console()
        
    # опция изменения задачи
    def change_option(self) -> None:
        task_id = id_validate_input('Введите id задачи, которую хотите изменить: ')
        if task_id:
            change_option = input(change_option_input_message)
            if change_option == '1':
                status = choice_validate_input('статус', status_choices, required=True)
                data = {'status': status}
                self.task_list.change(task_id, data)
                clean_console('Статус задачи успешно изменен')
            elif change_option == '2':
                data = task_input(change_task_fields_message)
                if data:
                    self.task_list.change(task_id, data)
                    clean_console('Поля задачи успешно изменены.')
            elif change_option == '3':
                clean_console()
            else:
                clean_console()
                print(option_error_message)

    # опция удаления задачи/задач    
    def delete_option(self) -> None:
        delete_option = input(delete_option_input_message)
        if delete_option == '1':
            task_id = id_validate_input('Введите id задачи: ')
            if task_id:
                self.task_list.delete(task_id=task_id)
                clean_console('Задача успешно удалена')
        elif delete_option == '2':
            category = input('Введите категорию: ')
            self.task_list.delete(category=category)
            clean_console(f'Задачи категории "{category}" успешно удалены.')
        elif delete_option == '3':
            clean_console()
        else:
            clean_console()
            print(option_error_message)

    def search_option(self) -> None:
        search_option = input(search_option_input_message)
        if search_option == '1':
            key_words = input('Введите ключевые слова через пробел: ')
            tasks = self.task_list.search(key_words=key_words)
            clean_console()
            show_tasks(tasks)
        elif search_option == '2':
            categories = input('Введите категории через пробел: ')
            tasks = self.task_list.search(categories=categories)
            clean_console()
            show_tasks(tasks)
        elif search_option == '3':
            status = choice_validate_input('статус', ['Выполнена', 'Не выполнена'])
            if status:
                tasks = self.task_list.search(status=status)
                clean_console()
                show_tasks(tasks)
        else:
            clean_console()
            print(option_error_message)
            
    # опция настроек программы
    def settings_option(self) -> None:
        print(f'Текущая директория для хранения данных: {self.file_path}')
        print(f'Текущий тип сохраняемых данных: {self.file_type}')
        
        setting_option = input(setting_option_input_message)
        if setting_option == '1':
            
            new_file_type_ind = choice_validate_input('тип данных', file_type_choices, required=True)
            if new_file_type_ind:
                new_file_type = file_type_choices[int(new_file_type_ind) - 1]
                if new_file_type == self.file_type:
                    print('Данный тип данных используется в данный момент')
                else:
                    all_data = self.file_manager.read()
                    os.remove(self.file_path)
                    self.file_type = new_file_type

                    if new_file_type== 'json':
                        new_file_manager = JsonFileManager(self.file_path)
                    elif new_file_type == 'csv':
                        new_file_manager = CsvFileManager(self.file_path)

                    new_file_manager.write(all_data)
                    self.file_manager = new_file_manager
                    self.task_list = TaskList(new_file_manager)
                    print('Тип данных успешно изменен')
            else:
                print(option_error_message)
            
    # основной
    def start(self) -> None:
        clean_console()
        print('Привет!')
        while True:
            print(option_list_message)
            option = input(option_input_message)
            clean_console()
            if option == '0':
                self.gen_tasks()
            elif option == '1':
                self.get_option()
            elif option == '2': 
                self.add_option()
            elif option == '3':
                self.change_option()
            elif option == '4':
                self.delete_option()
            elif option == '5':
                self.search_option()
            elif option == '6':
                self.settings_option()
            elif option == '7':
                break
            else:
                clean_console()
                print(option_error_message)
        print('До новых встреч!')