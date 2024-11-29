import json

status_choices = ['Выполнена', 'Не выполнена']
priority_choices = ['Высокий', 'Низкий', 'Средний']

def gen_task_id(tasks: list[dict]) -> str:
    ids = [int(task['id']) for task in tasks]
    if len(ids) == 0:
        return '0'
    return str(max(ids) + 1)

class Task:
    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.category = data["category"]
        self.due_date = data["due_date"]
        self.priority = data["priority"]
        self.status = data["status"]

    def show(self) -> None:
        status = status_choices[int(self.status)-1]
        priority = priority_choices[int(self.priority)-1]
        st = f'''\n{self.title}
Идентификатор: {self.id}
Описание: {self.description};
Категория: {self.category};
Дата: {self.due_date};
Приоритет: {priority};
Статус: {status};\n'''
        print(st)


class CsvFileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        pass

    def write(self, data):
        pass


class JsonFileManager:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> list[dict]:
        try:
            with open(self.file_path, 'r') as file:
                try:
                    data = json.load(file)
                except:
                    data = []
            return data
        except:
            data = []
            return data

    def write(self, data) -> None:
        with open(self.file_path, "w") as file:
            json.dump(data, file)
    
class TaskList:
    def __init__(self, file_manager: JsonFileManager | CsvFileManager) -> None:
        self.file_manager = file_manager

    def get(self, task_id: None | str = None, category: None | str = None) -> list[Task]:
        tasks = self.file_manager.read()
        if task_id:
            for task in tasks:
                if task['task_id'] == task_id:
                    return [Task(task)]
        if category:
            category_tasks = []
            for task in tasks:
                if task['category'] == category:
                    category_tasks.append(task)
            return [Task(task) for task in category_tasks]
        return [Task(task) for task in tasks]

    def add(self, task: dict) -> None:
        tasks = self.file_manager.read()
        new_task_task_id = gen_task_id(tasks)
        task['id'] = new_task_task_id
        tasks.append(task)
        self.file_manager.write(tasks)

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
    
    def search(self):
        pass