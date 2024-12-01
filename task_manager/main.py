from task_manager import TaskManager
from utils.system import find_file_info




file_info = find_file_info()

if file_info:
    interface = TaskManager(file_info[0], file_info[1])
    interface.start()
else:
    print('После исправления повторно запустите программу.')
