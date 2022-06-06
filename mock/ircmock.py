import irc


class IrcChannel(irc.IrcChannel):
    def __init__(self, twitch_host="irc.chat.twitch.tv", twitch_port=6667):
        self.irc = None

    def send(self, message):
        print(f"{message}\r\n")

    def receive(self, bytes_to_receive=1024):
        message: str = ":local.MockUser!local.MockUser@MockIF.tmi.twitch.tv PRIVMSG #MockChannel :" + str(input())
        return message
