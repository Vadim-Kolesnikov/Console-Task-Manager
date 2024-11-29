from datetime import datetime




# функция для запроса значений строковых полей задачи
def str_validate_input(str_name: str, required: bool = False) -> None | str:
    value = input(f'Введите {str_name}: ')
    if required:
        while len(value) == 0:
            print('Вы ввели пустую строку')
            value = input(f'Введите {str_name}, либо exit, если хотите вернутся в меню: ')
            if value == 'exit':
                return None
    return value


# функция для запроса дедлайна задачи
def date_validate_input(required: bool = False) -> None | str:
    str_date = input('Введите дату в формате dd.mm.yyyy')
    
    if required:
        while True:
            try:
                date = datetime.strptime(str_date, "%d.%m.%Y")
                if date < datetime.today():
                    print('Дедлайн не может быть установлен на прошедшую дату')
                    str_date = input('Введите дату в формате ')
                    continue
                break
            except:
                print('Введите корректную дату, либо exit, если хотите вернуться в меню')
                str_date = input('Введите дату в формате ')
                if str_date == 'exit':
                    return None
    else:
        while True and len(str_date) != 0:
            try:
                date = datetime.strptime(str_date, "%d.%m.%Y")
                if date < datetime.today():
                    print('Дедлайн не может быть установлен на прошедшую дату')
                    str_date = input('Введите дату в формате dd.mm.yyyy или пустую строку')
                    continue
                break
            except:
                print('Введите корректную дату, либо exit, если хотите вернуться в меню')
                str_date = input('Введите дату в формате dd.mm.yyyy или пустую строку')
                if str_date == 'exit':
                    return None
            
    return str_date


# функция для запроса полей с фиксированными значениями (статус, приоритет)
def choice_validate_input(str_name: str, acceptable_values: list[str], required: bool = False) -> None | str:
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


# функция для запроса id
def id_validate_input(message: str) -> None | str:
    task_id = input(message)
    while not task_id.isdigit():
        print('Введите числовое значение, либо exit, если хотите вернуться в меню')
        task_id = input(message)
        if task_id == 'exit':
            return None
    return task_id    
        

# функция для запроса полей необходимых для создания/изменения задачи
def task_input(message: str, all_required : bool = False) -> dict | None:
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

    due_date = date_validate_input(required=all_required)
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



