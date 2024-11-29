from task_manager import TaskManager
from utils.system_utils import search_data_path

data_path = search_data_path()
        
interface = TaskManager(data_path)

interface.start()
