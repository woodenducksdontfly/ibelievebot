import json

global stream_data_handler


class StreamDataHandler:
    def __init__(self):
        global stream_data_handler
        try:
            self.filename = "data/stream.json"
            with open(self.filename, 'r') as stream_data_file:
                self.stream_data = json.loads(stream_data_file.read())
        except:
            print("No stream data")
            self.stream_data = {"wrong": 0, "deaths": 0, "saves": 0}
        stream_data_handler = self

    def increment_wrongs(self):
        self.stream_data["wrong"] = self.stream_data.get("wrong", 0) + 1
        self.flush_data()

    def increment_deaths(self):
        self.stream_data["deaths"] = self.stream_data.get("deaths", 0) + 1
        self.flush_data()

    def increment_saves(self):
        self.stream_data["saves"] = self.stream_data.get("saves", 0) + 1
        self.flush_data()

    def get_wrongs(self):
        return self.stream_data["wrong"]

    def get_deaths(self):
        return self.stream_data["deaths"]

    def get_saves(self):
        return self.stream_data["saves"]

    def flush_data(self):
        with open(self.filename, 'w') as stream_data_file:
            stream_data_file.write(json.dumps(self.stream_data, sort_keys=True, indent=4))
