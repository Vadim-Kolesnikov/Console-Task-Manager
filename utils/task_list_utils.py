def convert(data, task_cls):
    if type(data) == list:
        return [(task_cls) for task in data]
    return [task_cls(data)]

def gen_id(tasks):
    ids = [int(task['id']) for task in tasks]
    if len(ids) == 0:
        return 0
    return str(max(ids) + 1)

def show_tasks(tasks):
    if len(tasks) == 0:
        print("\nНичего не найдено\n")
    else:
        for task in tasks:
            task.show()