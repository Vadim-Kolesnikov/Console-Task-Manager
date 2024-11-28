import os

def clean_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def show_tasks(tasks):
    if len(tasks) == 0:
        print("\nНичего не найдено\n")
    else:
        for task in tasks:
            task.show()
    
def task_input(message, is_all_required=False):
    print(message)
    dct = {}
    dct['id'] = '1'
    dct['title'] = input('Введите название задачи: ')
    dct['description'] = input('Введите описание задачи: ')
    dct['category'] = input('Введите категорию задачи: ')
    dct['due_date'] = '2024-11-30'
    dct['priority'] = input('Введите приоритет задачи: ')
    dct['status'] = input('Введите статус задачи: ')
    return dct

