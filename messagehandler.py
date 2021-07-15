import os
import pathlib
import importlib
from threading import Thread
from pprint import pprint
import re
import sys
import json
import requests


global message_handler_instance
global _elevated_users


def register(platform, command):
    #print("register {} [{}]".format(platform, command))

    def wrapper(function):
        message_handler_instance.register_command(command.lower(), platform, function)
        #print("{} registered".format(command))
        return function
    return wrapper


def register_timer(platform, name, function, channel, timeout):
    global message_handler_instance
    message_handler_instance.bots[platform].register_timer(name, function, channel, timeout)


def is_user_elevated(bot, channel, user):
    elevated_status = False
    mods = bot.get_moderators(channel[1:])
    if user in _elevated_users + mods:
        elevated_status = True
    return elevated_status


class MessageHandler(Thread):
    def __init__(self, message_mailbox):
        Thread.__init__(self)
        global message_handler_instance
        sys.path.append('watched')
        self.message_mailbox = message_mailbox
        self._files_last_read_time = {}
        self._loaded_modules = {}
        self._commands = {'all': {},
                          "twitter": {},
                          "twitch": {},
                          "discord": {},
                          'slack': {},
                          'youtube': {}}
        self.bots = {}
        self._ready = False
        # self.pattern = re.compile("([a-zA-Z]+:)(\(.+\):)*(.*:){1}( )(.*)")
        message_handler_instance = self

    def _load_files(self):
        for file_path in os.listdir('watched'):
            if pathlib.Path(file_path).suffix == '.py':
                self._load_python_module(file_path)
        self._ready = True

    def _watch_elevated_users(self):
        file_path = "data/elevated_users.json"
        mod_date = os.stat(file_path)[8]
        if mod_date > self._files_last_read_time.get(file_path, 0):
            print("Loading {}".format(file_path))
            global _elevated_users
            try:
                with open(file_path) as file:
                    _elevated_users = json.load(file)
                    self._files_last_read_time[file_path] = mod_date
            except:
                _elevated_users = {}
                self._files_last_read_time[file_path] = mod_date

    def _load_python_module(self, file_path):
        mod_date = os.stat("watched/{}".format(file_path))[8]
        if mod_date > self._files_last_read_time.get(file_path, 0):
            python_module = pathlib.Path(file_path).stem
            #print("Updating {} module".format(python_module))
            #print(python_module)
            #print(self._loaded_modules)
            if python_module in self._loaded_modules:
                importlib.reload(self._loaded_modules[python_module])
            else:
                self._loaded_modules[python_module] = importlib.import_module(python_module)
            importlib.invalidate_caches()
            self._files_last_read_time[file_path] = mod_date
            #pprint(self._commands)

    def register_command(self, command, platform, function):
        self._commands[platform][command.lower()] = function

    def register_bot(self, platform, bot):
        self.bots[platform] = bot

    def ready(self):
        return self._ready

    def run(self):
        self._load_files()
        self._watch_elevated_users()
        # Register currency handout timer
        register_timer('twitch',
                       'currency_handout_{}'.format('woodenducksdontfly'),
                       self._loaded_modules["gamble"]._give_everyone_currency,
                       channel=None,
                       timeout=200.0)
        # Syrup payout
        register_timer('twitch',
                       'syrup_handout_{}'.format('woodenducksdontfly'),
                       self._loaded_modules["gamble"]._give_everyone_syrup,
                       channel=None,
                       timeout=260.0)
        while True:
            """Receive text then reload then process"""
            receive = self.message_mailbox.get(block=True)
            """Reload files if necessary"""
            self._load_files()
            self._watch_elevated_users()

            platform = receive[0]
            from_user = receive[1]
            message = receive[2]
            channel = receive[3]
            threads = []
            try:
                if platform == "twitch":
                    callback = self._commands[platform].get(message.split(' ')[0].strip().lower(), None)
                    if callback:
                        threads.append(Thread(callback(self.bots[platform], from_user, message, channel)))
                elif platform == "discord":
                    callback = self._commands[platform].get(message.split(' ')[0].strip(), None)
                    if callback:
                        threads.append(Thread(callback(self.bots[platform], from_user, message, channel)))
                elif platform == "audio":
                    threads.append(Thread(self.bots['audio'].play_audio(self.bots[platform], from_user, message, channel)))
                elif platform == "announce":
                    send_to_platform = receive[4]
                    threads.append(Thread(self.bots[send_to_platform].write_to_chat(message, channel)))
            except Exception as e:
                print("Bad Function Call")
                print(e)

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
