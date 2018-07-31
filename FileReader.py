import logging


class FileReader(object):

    def __init__(self, file_path):
        self.file_path = file_path

    def get_content(self):
        with open(self.file_path, 'r') as file:
            data = file.read()
        logging.info("file data read")
        return data

