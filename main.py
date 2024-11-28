from interface import Interface
import os


listdir = os.listdir()

data_path = None
for path in listdir:
    if path.endswith('.json'):
        data_path = path
        
if not data_path:
    data_path = 'data.json'
        
interface = Interface(data_path)

interface.start()
