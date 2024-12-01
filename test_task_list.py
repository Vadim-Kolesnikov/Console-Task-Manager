from utils.test import gen_test_tasks, gen_file_manager
from task_list import *
from settings import TEST_CSV_FILE_NAME, TEST_JSON_FILE_NAME




def test_file_manager(tmpdir):
    '''Тест для файловых помощников'''

    json_file_manager = gen_file_manager(tmpdir, 'json', TEST_JSON_FILE_NAME)
    csv_file_manager = gen_file_manager(tmpdir, 'csv', TEST_CSV_FILE_NAME)

    assert json_file_manager.read() == []
    assert csv_file_manager.read() == []

    data = gen_test_tasks(10)

    json_file_manager.write(data)
    csv_file_manager.write(data)

    assert json_file_manager.read() == data
    assert csv_file_manager.read() == data


def test_add(tmpdir):
    '''Тест для функции добавления'''

    json_file_path = tmpdir.join(f'{TEST_JSON_FILE_NAME}.{'json'}')
    csv_file_path = tmpdir.join(f'{TEST_CSV_FILE_NAME}.{'csv'}')

    json_file_manager = JsonFileManager(json_file_path)
    csv_file_manager = CsvFileManager(csv_file_path)

    json_task_list = TaskList(json_file_manager)
    csv_task_list = TaskList(csv_file_manager)

    data = gen_test_tasks(10)
    for task in data:
        json_task_list.add(task)
        csv_task_list.add(task)

    assert json_file_manager.read() == data
    assert csv_file_manager.read() == data


def test_get(tmpdir):
    '''Тест для функции получения'''

    json_task_list = TaskList(gen_file_manager(tmpdir, 'json', TEST_JSON_FILE_NAME))
    csv_task_list = TaskList(gen_file_manager(tmpdir, 'csv', TEST_CSV_FILE_NAME))

    data = gen_test_tasks(5)
    for task in data:
        json_task_list.add(task)
        csv_task_list.add(task)
    
    assert [Task(task) for task in data] == json_task_list.get()
    assert [Task(task) for task in data] == csv_task_list.get()

    assert [Task(task) for task in data if task['category'] == 'category0'] == json_task_list.get(category='category0')
    assert [Task(task) for task in data if task['category'] == 'category0'] == csv_task_list.get(category='category0')

    assert [Task(task) for task in data if task['id'] == '0'] == json_task_list.get(task_id='0')
    assert [Task(task) for task in data if task['id'] == '0'] == csv_task_list.get(task_id='0')
 

def test_delete(tmpdir):
    '''Тест для функции удаления'''

    json_task_list = TaskList(gen_file_manager(tmpdir, 'json', TEST_JSON_FILE_NAME))
    csv_task_list = TaskList(gen_file_manager(tmpdir, 'csv', TEST_CSV_FILE_NAME))

    data = gen_test_tasks(10)
    for task in data:
        json_task_list.add(task)
        csv_task_list.add(task)

    json_task_list.delete(task_id='0')
    csv_task_list.delete(task_id='0')

    assert [Task(task) for task in data if task['id'] != '0'] == json_task_list.get()
    assert [Task(task) for task in data if task['id'] != '0'] == csv_task_list.get()

    json_task_list.delete(category='category1')
    csv_task_list.delete(category='category1')

    assert [Task(task) for task in data if task['id'] != '0' and task['category'] != 'category1'] == json_task_list.get()
    assert [Task(task) for task in data if task['id'] != '0' and task['category'] != 'category1'] == csv_task_list.get()
 

def test_change(tmpdir):
    '''Тест для функции изменения'''

    json_task_list = TaskList(gen_file_manager(tmpdir, 'json', TEST_JSON_FILE_NAME))
    csv_task_list = TaskList(gen_file_manager(tmpdir, 'csv', TEST_CSV_FILE_NAME))

    data = gen_test_tasks(10)
    for task in data:
        json_task_list.add(task)
        csv_task_list.add(task)

    json_task_list.change(task_id='0', data={'title': 'new_title0'})
    csv_task_list.change(task_id='0', data={'title': 'new_title0'})

    data[0]['title'] = 'new_title0'

    assert [Task(task) for task in data] == json_task_list.get()
    assert [Task(task) for task in data] == csv_task_list.get()


def test_search(tmpdir):
    '''Тест для функции поиска'''

    json_task_list = TaskList(gen_file_manager(tmpdir, 'json', TEST_JSON_FILE_NAME))
    csv_task_list = TaskList(gen_file_manager(tmpdir, 'csv', TEST_CSV_FILE_NAME))

    data = gen_test_tasks(10)
    for task in data:
        json_task_list.add(task)
        csv_task_list.add(task)

    assert [Task(task) for task in data if task['title'] == 'title1' or task['title'] == 'title2'] == json_task_list.search(key_words='title1 title2')
    assert [Task(task) for task in data if task['title'] == 'title1' or task['title'] == 'title2'] == csv_task_list.search(key_words='title1 title2')
    
    assert [Task(task) for task in data if task['category'] == 'category0'] == json_task_list.search(categories='category0')
    assert [Task(task) for task in data if task['category'] == 'category0'] == csv_task_list.search(categories='category0')
    
    assert [Task(task) for task in data if task['status'] == '0'] == json_task_list.search(status='0')
    assert [Task(task) for task in data if task['status'] == '0'] == csv_task_list.search(status='0')