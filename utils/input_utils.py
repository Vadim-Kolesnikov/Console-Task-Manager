def str_validate_input(str_name, required=False):
    value = input(f'Введите {str_name}: ')
    if required:
        while len(value) == 0:
            print('Вы ввели пустую строку')
            value = input(f'Введите {str_name}, либо exit, если хотите вернутся в меню: ')
            if value == 'exit':
                return None
    return value

def date_validate_input(str_name, required=False):
    value = input(f'Введите {str_name}: ')
    if required:
        while len(value) == 0:
            print('Вы ввели пустую строку')
            value = input(f'Введите {str_name}, либо exit, если хотите вернутся в меню: ')
            if value == 'exit':
                return None
    return value

def choice_validate_input(str_name, acceptable_values, required=False):
    acceptable_values_str = ' '.join([f'{i} - {v};' for i, v in enumerate(acceptable_values, 1)])
    acceptable_values_options = [str(i + 1) for i in range(len(acceptable_values))]
    value = input(f'Введите {str_name} ({acceptable_values_str}): ')
    if required:
        while value.lower() not in acceptable_values_options:
            print('Вы ввели неверное значение')
            value = input(f'Введите {str_name} ({acceptable_values_str}), либо exit, если хотите вернутся в меню: ')
            if value == 'exit':
                return None
    else:
        while (value.lower() not in acceptable_values_options) and (len(value) > 0):
            print('Вы ввели неверное значение')
            value = input(f'Введите {str_name} ({acceptable_values_str}), либо exit, если хотите вернутся в меню: ')
            if value == 'exit':
                return None
    return value
        


def task_input(message, all_required=False):
    print(message)
    dct = {}
   
    title = str_validate_input('название задачи', required=all_required)
    if not title:
        return None
    dct['title'] = title
        
    description = str_validate_input('описание задачи', required=all_required)
    if not description:
        return None
    dct['description'] = description

    category = str_validate_input('категорию задачи', required=all_required)
    if not category:
        return None
    dct['category'] = category

    due_date = date_validate_input('дедлайн задачи', required=all_required)
    if not due_date:
        return None
    dct['due_date'] = due_date

    priority = choice_validate_input('приоритет задачи', ['Высокий', 'Низкий', 'Средний'], required=all_required)
    if not priority:
        return None
    dct['priority'] = priority

    status = choice_validate_input('статус задачи', ['Выполнена', 'Не выполнена'], required=all_required)
    if not status:
        return None
    dct['status'] = status

    return dct


def id_validate_input(message):
    task_id = input(message)
    while not task_id.is_digit():
        print('Введите числовое значение, либо exit, если хотите вернуться в меню')
        task_id = input(message)
        if task_id == 'exit':
            return None
    return task_id    