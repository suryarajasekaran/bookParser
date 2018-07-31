import json
import logging


class FileWriter(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def write_content(self, data):
        logging.info("writing generated json struct data to file")
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
