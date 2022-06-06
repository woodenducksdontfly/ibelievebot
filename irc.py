import socket
from datetime import datetime
import html
import customlogger
import logging


class IrcChannel:

    def __init__(self, twitch_host="irc.chat.twitch.tv", twitch_port=6667):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((twitch_host, twitch_port))
        self.logger = customlogger.get_logger(__name__)

    def send(self, message):
        formatted_message = f"[{datetime.now()}] {message}"
        print(formatted_message)
        self.logger.log(logging.INFO, formatted_message.rstrip("\r\n"))
        self.irc.send(html.unescape(message).encode('utf-8'))

    def receive(self, bytes_to_receive=1024):
        message = self.irc.recv(bytes_to_receive).decode()
        formatted_message = f"[{datetime.now()}] {message}"
        print(formatted_message)
        self.logger.log(logging.INFO, formatted_message.rstrip("\r\n"))
        return message
