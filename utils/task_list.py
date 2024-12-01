def prep_text(text: str, string_len: int) -> str:
    '''
    Преобразует поля задачи
    в строку/строки для вывода в консоль
    '''

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


def gen_task_id(tasks: list[dict]) -> str:
    '''Генерирует id задачи'''

    ids = [int(task['id']) for task in tasks]
    if len(ids) == 0:
        return '0'
    return str(max(ids) + 1)


def show_tasks(tasks: list, message: str = 'Задачи:') -> None:
    '''Вспомогательная функция для вывода задач'''

    if len(tasks) > 0:
        print(message)
        for task in tasks:
            print(task, '\n')
        print('\n')
    else:
        print('\nНичего не найдено\n')


def is_key_word_in_task(task: dict, key_word_list: list[str]) -> bool:
    '''
    Проверяет содержатся ли ключевые слова из списка
    в каком либо из полей задачи
    '''

    task_fields = ['title', 'description', 'category']
    
    for field in task_fields:
        field_words = [word.strip().lower() for word in task[field].split(' ')]
        for key_word in key_word_list:
            if key_word in field_words:
                return True
        
    return False