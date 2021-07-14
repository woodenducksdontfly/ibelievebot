import socket
from datetime import datetime
import html


class IrcChannel:

    def __init__(self, twitch_host="irc.chat.twitch.tv", twitch_port=6667):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((twitch_host, twitch_port))

    def send(self, message):
        print("[{}] {}".format(datetime.now(), message))
        #if "PRIVMSG" not in message:
        self.irc.send(html.unescape(message).encode('utf-8'))

    def receive(self, bytes_to_receive=1024):
        message = self.irc.recv(bytes_to_receive).decode()
        print("[{}] {}".format(datetime.now(), message))
        return message
