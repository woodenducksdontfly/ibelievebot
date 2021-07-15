import json
import os

global file_handler


class StaticFileHandler:
    def __init__(self):
        global file_handler
        self.file_data = {}
        try:
            os.mkdir("data/read_only")
        except FileExistsError as e:
            pass
        for file in os.listdir("data/read_only"):
            self.load_data_file(file)
        file_handler = self

    def load_data_file(self, filename):
        try:
            with open('data/read_only/{}'.format(filename), 'r') as file:
                self.file_data[filename] = json.loads(file.read())
        except Exception:
            print("Problem while reading {}".format(filename))

    def get_file_data(self, filename):
        try:
            data = self.file_data[filename]
        except:
            data = []
        return data

    # TODO remove?
    def _flush_data(self, filename):
        with open('data/{}'.format(filename), 'w') as file:
            file.write(json.dumps(self.file_data[filename], sort_keys=True, indent=4))
