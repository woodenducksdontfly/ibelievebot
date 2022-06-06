import json
import datetime
import math
import os

global user_data_handler


class UserDataHandler:
    def __init__(self):
        global user_data_handler
        try:
            self.filename = "data/user_data.json"
            self._files_last_read_time = 0
            self.gold_waffle_price = 1000000000
            self._load_user_data()
        except:
            print("No user data")
            self.user_data = {}
        user_data_handler = self

    def _load_user_data(self):
        mod_date = os.stat(self.filename)[8]
        if mod_date > self._files_last_read_time:
            with open(self.filename, 'r') as user_data_file:
                self.user_data = json.loads(user_data_file.read())
            self._files_last_read_time = mod_date

    def get_and_init_user(self, username):
        user = self.user_data.get(username)
        if not user:
            self.user_data[username] = {"balance": 69420,
                                        "syrup_balance": 10,
                                        "first_chat": str(datetime.datetime.now(tz=datetime.timezone.utc)),
                                        "golden_waffles": 0,
                                        "club_status": None}
            user = self.user_data.get(username)
            self.flush_data()
        return user

    def get_syrup_balance(self, username):
        user = self.get_and_init_user(username)
        return user.get("syrup_balance", 10)

    def get_balance(self, username):
        user = self.get_and_init_user(username)
        return user.get("balance")

    def add_syrup_balance(self, username, value):
        self.add_syrup_balance_wait_for_flush(username, value)
        self.flush_data()

    def add_balance(self, username, value):
        self.add_balance_wait_for_flush(username, value)
        self.flush_data()

    def add_syrup_balance_wait_for_flush(self, username, value):
        user = self.get_and_init_user(username)
        user['syrup_balance'] = user.get("syrup_balance", 10) + value

    def add_balance_wait_for_flush(self, username, value):
        user = self.get_and_init_user(username)
        user['balance'] = user.get("balance", 69420) + value

    def subtract_syrup_balance(self, username, value):
        user = self.get_and_init_user(username)
        user['syrup_balance'] = user.get("syrup_balance", 10) - value
        self.flush_data()

    def subtract_balance(self, username, value):
        user = self.get_and_init_user(username)
        user['balance'] = user.get("balance", 10) - value
        self.flush_data()

    def get_top_users_by_balance(self):
        return sorted(self.user_data, key=lambda user: self.get_balance(user), reverse=True)

    def get_top_syrup_users_by_balance(self):
        return sorted(self.user_data, key=lambda user: self.get_syrup_balance(user) + (self.get_golden_waffles(user) * self.gold_waffle_price), reverse=True)

    def get_bottom_users_by_balance(self):
        return sorted(self.user_data, key=lambda user: self.get_balance(user) + (self.get_golden_waffles(user) * self.gold_waffle_price))

    def get_club_status(self, username):
        user = self.get_and_init_user(username)
        return user.get("club_status")

    def get_golden_waffles(self, username):
        user = self.get_and_init_user(username)
        golden_waffles = user.get("golden_waffles", 0)
        return golden_waffles

    def add_gold_waffles(self, username):
        user = self.get_and_init_user(username)
        purchasable_waffles = max(math.floor(user["balance"] / self.gold_waffle_price), 0)
        user["balance"] = user["balance"] - (purchasable_waffles * self.gold_waffle_price)
        user['golden_waffles'] = user.get("golden_waffles", 0) + purchasable_waffles
        self.update_club_status_wait_for_flush(username)
        self.flush_data()

    def remove_gold_waffle(self, username):
        user = self.get_and_init_user(username)
        if 10 > user['golden_waffles'] > 0:
            user['golden_waffles'] = user['golden_waffles'] - 1
            user["balance"] = user["balance"] + self.gold_waffle_price
            self.update_club_status_wait_for_flush(username)
            self.flush_data()

    def update_club_status_wait_for_flush(self, username):
        user = self.get_and_init_user(username)
        golden_waffles = user.get("golden_waffles", 0)
        if golden_waffles >= 10:
            user['club_status'] = "God"
            user["balance"] = 0
        elif 10 > golden_waffles > 0:
            user['club_status'] = f"Level {golden_waffles} Member"
        else:
            user['club_status'] = None

    def flush_data(self):
        with open(self.filename, 'w') as user_data_file:
            user_data_file.write(json.dumps(self.user_data, sort_keys=True, indent=4))
