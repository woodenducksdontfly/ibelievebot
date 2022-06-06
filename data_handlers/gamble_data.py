import json
import datetime
import os

global gamble_data_handler


class GambleDataHandler:
    def __init__(self):
        global gamble_data_handler
        self.file_last_updated = 0
        try:
            self.roll_filename = "data/tmp_roll.json"
            with open(self.roll_filename, 'r') as roll_file:
                self.roll_data = json.loads(roll_file.read())
        except Exception as e:
            print("No roll data")
            self.roll_data = {}
        self.recent_chatters = {}
        gamble_data_handler = self

    def is_valid_roll(self, username, channel):
        now = datetime.datetime.now()
        user_data = self.roll_data.get(username, {})
        last_roll = json.loads(user_data.get(channel)) if user_data.get(channel) else "2020-07-08"
        no_roll_since = now - datetime.datetime.fromisoformat(last_roll)
        if no_roll_since.total_seconds() >= 86400:  # 24 hours in seconds
            user_data[channel] = json.dumps(now.isoformat(), default=str)
            self.roll_data[username] = user_data
            self.flush_data()
            return True

    def add_recent_chatter(self, username, channel):
        if not self.recent_chatters.get(channel):
            self.recent_chatters[channel] = set()
        self.recent_chatters[channel].add(username)

    def remove_recent_chatter(self, username, channel):
        if not self.recent_chatters.get(channel):
            self.recent_chatters[channel] = set()
        self.recent_chatters[channel].remove(username)

    def get_recent_chatters(self, channel):
        if not self.recent_chatters.get(channel):
            self.recent_chatters[channel] = set()
        return self.recent_chatters[channel]

    def flush_data(self):
        mod_date = os.stat(self.roll_filename)[8]
        with open(self.roll_filename, 'w') as roll_file:
            roll_file.write(json.dumps(self.roll_data, sort_keys=True, indent=4))
            self.file_last_updated = mod_date
