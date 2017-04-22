import json
import os.path
from threading import Lock


class JSONReaderWriter:

    json_path = ""
    file_mutex = Lock()

    def __init__(self, f_path):
        self.json_path = f_path

        
    def write(self, data):
        self.file_mutex.acquire()
        json_file = open(self.json_path, 'w')
        json.dump(data, json_file, indent=4, sort_keys=True)
        json_file.close()
        self.file_mutex.release()


    def read(self):
        self.file_mutex.acquire()
        json_file = open(self.json_path, 'r')
        parsed_data = json.loads(json_file.read())
        json_file.close()
        self.file_mutex.release()
        return parsed_data


    def exists(self):
        return os.path.exists(self.json_path)