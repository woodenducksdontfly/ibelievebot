import irc


class IrcChannel(irc.IrcChannel):
    def __init__(self, twitch_host="irc.chat.twitch.tv", twitch_port=6667):
        self.irc = None

    def send(self, message):
        print("{}\r\n".format(message))
        #print(message.encode('utf-8')+"\r\n")

    def receive(self, bytes_to_receive=1024):
        return ":local.MockUser!local.MockUser@MockIF.tmi.twitch.tv PRIVMSG #MockChannel :" + input()
