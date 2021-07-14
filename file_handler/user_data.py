import json
import datetime

global user_data_handler


class UserDataHandler:
    def __init__(self):
        global user_data_handler
        try:
            self.filename = "data/user_data.json"
            with open(self.filename, 'r') as user_data_file:
                self.user_data = json.loads(user_data_file.read())
        except:
            print("No user data")
            self.user_data = {}
        user_data_handler = self

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
        return sorted(self.user_data, key=lambda user: self.get_syrup_balance(user), reverse=True)

    def get_bottom_users_by_balance(self):
        return sorted(self.user_data, key=lambda user: self.get_balance(user))

    def get_club_status(self, username):
        user = self.get_and_init_user(username)
        return user.get("club_status")

    def update_club_status(self, username):
        user = self.get_and_init_user(username)
        level_value = user.get("balance") % 1000000000
        previous_level = user.get("club_status")
        if level_value >= 10:
            user['club_status'] = "God"
        elif level_value > 0:
            user['club_status'] = level_value
        elif previous_level:
            if previous_level > level_value:
                user['club_status'] = "revoked"
        else:
            pass

    def flush_data(self):
        with open(self.filename, 'w') as user_data_file:
            user_data_file.write(json.dumps(self.user_data, sort_keys=True, indent=4))
