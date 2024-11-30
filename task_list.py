from utils.system import JsonFileManager, CsvFileManager
from settings import status_choices, priority_choices


def prep_text(text, string_len):
    words = text.split(' ')
    strings = []
    string = '| '
    for word in words:
        if len(string + word + " ") >= (string_len - 1):
            if len(string) < (string_len - 1):
                string += ' ' * (string_len - 1 - len(string))
            string += '|'
            strings.append(string)
            string = '| '
        string += word + " " 
    if not string.endswith('|'):
        if len(string) < (string_len - 1):
            string += ' ' * (string_len - 1 - len(string))
        string += '|'
    strings.append(string)
    return '\n'.join(strings)




# функция генерации id задачи
def gen_task_id(tasks: list[dict]) -> str:
    ids = [int(task['id']) for task in tasks]
    if len(ids) == 0:
        return '0'
    return str(max(ids) + 1)


# класс для более комфортного взаимодействия со словарями (задачами)
class Task:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.category = data["category"]
        self.due_date = data["due_date"]
        self.priority = data["priority"]
        self.status = data["status"]

    # функция выведения информации о задаче в консоль
    def show(self, str_ln: int) -> None:
        status = status_choices[int(self.status)-1]
        priority = priority_choices[int(self.priority)-1]
  
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
        print(st)


def show_tasks(tasks: list[Task], message: str = 'Задачи:') -> None:
    if len(tasks) > 0:
        print(message)
        for task in tasks:
            task.show(30)
        print('\n')
    else:
        print('\nНичего не найдено\n')

def is_key_word_in_task(task: dict, key_word_list: list[str]) -> bool:
    task_fields = ['title', 'description', 'categoru']
    
    for field in task_fields:
        field_words = [word.strip().lower() for word in task[field].split(' ')]
        for key_word in key_word_list:
            if key_word in field_words:
                return True
        
    return False




# класс для взаимодействия с базой данных (в данном случае с файлом .json/.csv)
class TaskList:
    def __init__(self, file_manager: JsonFileManager | CsvFileManager) -> None:
        self.file_manager = file_manager

    # возращает все записанные задачи, если не переданы никакие аргументы
    # если передан "task_id", вовращается задача с соответствующим id
    # если передан "category", возвращаются задачи соответвующей категории
    def get(self, task_id: None | str = None, category: None | str = None) -> list[Task]:
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


    # добавляет задачу в базу данных
    def add(self, task: dict) -> None:
        tasks = self.file_manager.read()
        new_task_task_id = gen_task_id(tasks)
        task['id'] = new_task_task_id
        tasks.append(task)
        self.file_manager.write(tasks)

    # изменяет задачу
    def change(self, task_id: str, data: dict) -> None:
        tasks = self.file_manager.read()
        for task in tasks:
            if int(task['id']) == int(task_id):
                for key in task.keys():
                    if key in data.keys():
                        if len(data[key]) > 0:
                            task[key] = data[key] 
                self.file_manager.write(tasks)
                break

    # удаляет все записанные задачи, если не переданы никакие аргументы (не готово еще)
    # если передан "task_id", удаляется задача с соответствующим id
    # если передан "category", удаляются задачи соответвующей категории
    def delete(self, task_id: str | None = None, category: str | None = None) -> None:
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
        tasks = self.file_manager.read()
        if key_words:
            searched_tasks = []
            key_list = [key.strip().lower() for key in key_words.split(' ')]
            for task in tasks:
                if is_key_word_in_task(task, key_list):
                    searched_tasks.append(task)
            return searched_tasks
        elif key_words:
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
        