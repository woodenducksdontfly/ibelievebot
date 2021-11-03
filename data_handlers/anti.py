import json
import os

global anti_data_handler


class AntiDataHandler:
    def __init__(self):
        global anti_data_handler
        self.file_last_updated = 0
        try:
            self.filename = "data/user_registry.json"
            self.reload_users()
        except:
            print("No stream data")
            self.user_registry = []
        anti_data_handler = self

    def reload_users(self):
        mod_date = os.stat(self.filename)[8]
        if mod_date > self.file_last_updated:
            with open(self.filename, 'r') as user_registry_file:
                self.user_registry = json.loads(user_registry_file.read())
                self.file_last_updated = mod_date

    def is_registered(self, username):
        return username in self.user_registry

    def register(self, username):
        if username not in self.user_registry:
            self.user_registry.append(username)
            self.flush_data()

    def flush_data(self):
        mod_date = os.stat(self.filename)[8]
        with open(self.filename, 'w') as user_registry_file:
            user_registry_file.write(json.dumps(self.user_registry, sort_keys=True, indent=4))
            self.file_last_updated = mod_date
