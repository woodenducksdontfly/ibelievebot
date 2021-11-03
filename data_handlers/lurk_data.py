import json
import datetime
import os

global lurk_data_handler


class LurkDataHandler:
    def __init__(self):
        global lurk_data_handler
        self.lurkers = {}
        lurk_data_handler = self

    def add_lurker(self, username, channel):
        self.lurkers[channel] = self.lurkers.get(channel, set())
        self.lurkers[channel].add(username)

    def remove_lurker(self, username, channel):
        self.lurkers[channel] = self.lurkers.get(channel, set())
        self.lurkers[channel].remove(username)

    def get_lurkers(self, channel):
        return self.lurkers.get(channel, set())
