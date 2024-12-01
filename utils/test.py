from utils.system import JsonFileManager, CsvFileManager


def gen_test_tasks(task_num: int) -> list[dict]:
    '''Генерирует тестовые задания'''

    tasks = []
    for i in range(task_num):
        task = {
            "id": str(i), 
            "title": f"title{i}", 
            "description": f"description{i}", 
            "category": f"category{i % 2}",
            "due_date": f"22.04.2025", 
            "priority": f"{i % 2}", 
            "status": f"{i % 2}"
        }
        tasks.append(task)
    return tasks


def gen_file_manager(tmpdir, file_type: str, file_name: str) -> JsonFileManager | CsvFileManager:
    '''Создает файловый менеджер'''

    file_path = tmpdir.join(f'{file_name}.{file_type}')
    if file_type == 'json':
        file_manager = JsonFileManager(file_path)
    elif file_type == 'csv':
        file_manager = CsvFileManager(file_path)
    return file_manager