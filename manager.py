import json

class Task:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.category = data["category"]
        self.due_date = data["due_date"]
        self.priority = data["priority"]
        self.status = data["status"]

    def show(self):
        st = f'''\n{self.title}
Описание: {self.description};
Категория: {self.category};
Дата: {self.due_date};
Приоритет: {self.priority};
Статус: {self.status};\n'''
        print(st)


def convert(data):
    if type(data) == list:
        return [Task(task) for task in data]
    return [Task(data)]


class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
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

    def write(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file)


class TaskManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def get(self, id=None, category=None):
        tasks = self.file_manager.read()
        if id:
            for task in tasks:
                if task['id'] == id:
                    return convert(task)
        if category:
            category_tasks = []
            for task in tasks:
                if task['category'] == category:
                    category_tasks.append(task)
            return convert(category_tasks)
        return convert(tasks)

    def add(self, task):
        tasks = self.file_manager.read()
        tasks.append(task)
        self.file_manager.write(tasks)

    def change(self, id, data):
        tasks = self.file_manager.read()
        for task in tasks:
            if int(task['id']) == int(id):
                for key in task.keys():
                    if key in data.keys():
                        if len(data[key]) > 0:
                            task[key] = data[key] 
                self.file_manager.write(tasks)
                break

    def delete(self, id=None, category=None):
        tasks = self.file_manager.read()
        if id:
            for task in tasks:
                if task['id'] == id:
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




