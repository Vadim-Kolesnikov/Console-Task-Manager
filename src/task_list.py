from utils.system import JsonFileManager, CsvFileManager
from settings import STATUS_CHOICES, PRIORITY_CHOICES
from utils.task_list import *




class Task:
    '''
    Класс для более комфортного
    взаимодействия со словарями (задачами)
    '''

    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.category = data["category"]
        self.due_date = data["due_date"]
        self.priority = data["priority"]
        self.status = data["status"]

    def __eq__(self, other):
        '''
        Метод переопределен дабы проверка
        в тестах работа корректно
        '''
        
        if isinstance(other, Task):
            if not (self.id == other.id):
                return False
            if not (self.title == other.title):
                return False
            if not (self.description == other.description):
                return False
            if not (self.category == other.category):
                return False
            if not (self.due_date == other.due_date):
                return False
            if not (self.priority == other.priority):
                return False
            if not (self.status == other.status):
                return False
            return True
        return False

    def __str__(self) -> None:
        '''
        Метод переопределен для 
        удобства вывода задачи в консоль
        '''

        status = STATUS_CHOICES[int(self.status)-1]
        priority = PRIORITY_CHOICES[int(self.priority)-1]
        str_ln = 30
        sep_char = '-'
        side_char = '|'
        st = f'''
+{(str_ln - 2) * sep_char}+
{prep_text("Название: " + self.title, 30)}
{side_char}{(str_ln - 2) * sep_char}{side_char}
{prep_text("Идентификатор: " + self.id, str_ln)}
{side_char}{(str_ln - 2) * sep_char}{side_char}
{prep_text("Описание: " + self.description, str_ln)}
{side_char}{(str_ln - 2) * sep_char}{side_char}
{prep_text("Категория: " + self.category, str_ln)}
{side_char}{(str_ln - 2) * sep_char}{side_char}
{prep_text("Дата: " + self.due_date, str_ln)}
{side_char}{(str_ln - 2) * sep_char}{side_char}
{prep_text("Приоритет: " + priority, str_ln)}
{side_char}{(str_ln - 2) * sep_char}{side_char}
{prep_text("Статус: " + status, str_ln)}
+{(str_ln - 2) * sep_char}+'''
        return st


class TaskList:
    '''
    Класс для взаимодействия с базой данных 
    (в данном случае с файлом .json/.csv)
    '''
    
    def __init__(self, file_manager: JsonFileManager | CsvFileManager) -> None:
        self.file_manager = file_manager

    def get(self, task_id: None | str = None, category: None | str = None) -> list[Task]:
        '''
        Возращает все записанные задачи, если не переданы никакие аргументы
        если передан "task_id", вовращается задача с соответствующим id
        если передан "category", возвращаются задачи соответвующей категории
        '''

        tasks = self.file_manager.read()
        if task_id:
            for task in tasks:
                if task['id'] == task_id:
                    return [Task(task)]
        if category:
            category_tasks = []
            for task in tasks:
                if task['category'].lower() == category.lower():
                    category_tasks.append(task)
            return [Task(task) for task in category_tasks]
        return [Task(task) for task in tasks]

    def add(self, task: dict, is_gen_task_id: bool = True) -> None:
        '''Добавляет задачу в базу данных'''

        tasks = self.file_manager.read()
        if is_gen_task_id:
            new_task_id = gen_task_id(tasks)
            task['id'] = new_task_id
        tasks.append(task)
        self.file_manager.write(tasks)

    def change(self, task_id: str, data: dict) -> None:
        '''Изменяет задачу'''

        tasks = self.file_manager.read()
        for task in tasks:
            if int(task['id']) == int(task_id):
                for key in task.keys():
                    if key in data.keys():
                        if len(data[key]) > 0:
                            task[key] = data[key] 
                self.file_manager.write(tasks)
                break

    def delete(self, task_id: str | None = None, category: str | None = None) -> None:
        '''
        Удаляет все записанные задачи, если не переданы никакие аргументы (не готово еще)
        если передан "task_id", удаляется задача с соответствующим id
        если передан "category", удаляются задачи соответвующей категории
        '''

        tasks = self.file_manager.read()
        if task_id:
            for task in tasks:
                if task['id'] == task_id:
                    tasks.remove(task)
                    self.file_manager.write(tasks)
                    break
        elif category:
            for task in tasks:
                if task['category'] == category:
                    tasks.remove(task)
            self.file_manager.write(tasks)
    
    def search(self, key_words: str | None = None, 
               categories: str | None = None,
               status: str | None = None) -> list[Task]:
        '''
        Находит задачи 
        по категориям / ключевым словам / статусу
        '''

        tasks = self.file_manager.read()
        if key_words:
            searched_tasks = []
            key_list = [key.strip().lower() for key in key_words.split(' ')]
            for task in tasks:
                if is_key_word_in_task(task, key_list):
                    searched_tasks.append(task)
            return [Task(task) for task in searched_tasks]
        elif categories:
            category_list = [cat.strip().lower() for cat in categories.split(' ')]
            category_tasks = []
            for task in tasks:
                if task['category'].lower() in category_list:
                    category_tasks.append(task)
            return [Task(task) for task in category_tasks]
        elif status:
            status_tasks = []
            for task in tasks:
                if task['status'] == status:
                    status_tasks.append(task)
            return [Task(task) for task in status_tasks]