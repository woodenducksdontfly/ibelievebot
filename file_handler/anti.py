import json

global anti_data_handler


class AntiDataHandler:
    def __init__(self):
        global anti_data_handler
        try:
            self.filename = "data/user_registry.json"
            with open(self.filename, 'r') as user_registry_file:
                self.user_registry = json.loads(user_registry_file.read())
        except:
            print("No stream data")
            self.user_registry = []
        anti_data_handler = self

    def is_registered(self, username):
        return username in self.user_registry

    def register(self, username):
        if username not in self.user_registry:
            self.user_registry.append(username)
            self.flush_data()

    def flush_data(self):
        with open(self.filename, 'w') as user_registry_file:
            user_registry_file.write(json.dumps(self.user_registry, sort_keys=True, indent=4))
