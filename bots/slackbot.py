from threading import Thread
from slackclient import SlackClient


class SlackBot(Thread):
    def __init__(self, slack_token, message_mailbox):
        Thread.__init__(self, daemon=True)
        self.slack_token = slack_token
        self.message_mailbox = message_mailbox

    def run(self):
        SlackClient(self.slack_token)
