from pprint import pprint
import time
import sys
import re
from threading import Thread, Timer
import logging
import utils.textutil as textutil
import requests
import json
from bots.bot import Bot
import importlib
import copy
from data_handlers import anti, user_data, gamble_data, lurk_data

class TwitchBot(Thread, Bot):

    def __init__(self, streamer, twitch_client_id, twitch_oauth, twitch_api_oauth, message_mailbox, mock_irc=False, go_live_notification=True):
        Thread.__init__(self)
        if mock_irc:
            print("mock irc")
            irc = importlib.import_module('mock.ircmock')
        else:
            irc = importlib.import_module('irc')

        self.password = twitch_oauth
        self.greeting = "Hello"
        self.nickname = "ibelievebot"
        sys.path.insert(0, 'watched')
        self._files_last_read_time = {}
        self._loaded_modules = {}
        self._commands = {}
        self.timers = {}
        self.streamer = streamer
        self.channels = []
        self.penalty_mode = 'disabled'
        self.penalty_timeout = 5
        self.go_live_notification = go_live_notification
        try:
            with open("data/join_channels.json", 'r') as f:
                self.channels = json.load(f) # ["#{}".format(channel_name) for channel_name in json.load(f)]
        except:
            with open("data/join_channels.json", 'w') as f:
                print("You should update data/join_channels.json")
                f.write('["woodenducksdontfly"]\n')
                self.channels = "woodenducksdontfly"
        self.message_mailbox = message_mailbox
        self.irc_channel = irc.IrcChannel("irc.chat.twitch.tv", 6667)
        # Message format from twitch irc
        #:ibelievebot!ibelievebot@ibelievebot.tmi.twitch.tv PRIVMSG #woodenducksdontfly :no
        self.pattern = re.compile("(:)(.*)(![^\s]+ )([^\s]+ )(#){1}([^\s]+ )(:)(.*)")
        self.api_hdrs = {"Accept": "application/vnd.twitchtv.v5+json",
                         "Client-ID": "{}".format(twitch_client_id),
                         "Authorization": "Bearer {}".format(twitch_api_oauth)}
        self.long_live_live = {}
        for channel in self.channels:
            self.long_live_live[channel] = False
        self.streamer_api_tokens = {}
        try:
            with open('data/streamer_api_tokens.json', 'r') as f:
                self.streamer_api_tokens = json.load(f)
        except:
            api_tokens = {"woodenducksdontfly": ""}
            with open('data/streamer_api_tokens.json', 'w') as f:
                f.write(json.dumps(api_tokens, sort_keys=True, indent=4))
            self.streamer_api_tokens = api_tokens
        print("New BOT")

    def write_to_system(self, message):
        self.irc_channel.send(message)

    def write_to_chat(self, message, channel=None):
        self.write_to_system(f"PRIVMSG #{channel} :{message}\r\n")

    def call(self, cmd, channel=None):
        print(cmd)
        exec(cmd)
        print("done")

    def register_timer(self, name, function, channel, timeout):
        if channel:
            if self.timers.get(name):
                self.timers[name].cancel()
            self.timers[name] = Timer(timeout, function, [self, channel, channel, channel])
            self.timers[name].daemon = True
            self.timers[name].start()
        else:
            for my_channel in self.channels:
                if self.timers.get("{}_{}".format(name, my_channel)):
                    self.timers["{}_{}".format(name, my_channel)].cancel()
                self.timers["{}_{}".format(name, my_channel)] = Timer(timeout, function, [self, my_channel, my_channel, my_channel])
                self.timers["{}_{}".format(name, my_channel)].daemon = True
                self.timers["{}_{}".format(name, my_channel)].start()

    def go_live(self, thread, sent_by, msg_txt, channel):
        self.register_timer('check_for_live_{}'.format(channel), self.go_live, channel, 600.0)
        # self.register_timer('check_for_live', self.go_live, 120.0)
        resp = requests.get(url="https://api.twitch.tv/helix/search/channels?query={}".format(channel),
                            headers=self.api_hdrs)
        if resp and resp.status_code == 200:
            resp_json = json.loads(resp.content)
            try:
                result = resp_json['data'][0]
                if result['broadcaster_login'] == channel:
                    m_is_live = result['is_live']
                    # Last seen playing result['game_name']
                    if self.long_live_live[channel] != m_is_live and m_is_live:
                        # @Watch role (@ user, @& role, # channel)
                        if self.go_live_notification:
                            self.message_mailbox.put(('announce',
                                                      self.nickname,
                                                      "<@&830878319650144306> {0} is live! \nhttps://www.twitch.tv/{0}".format(channel),
                                                      "718300493407060018",
                                                      "discord"))
                        self.long_live_live[channel] = True
                    elif not m_is_live:
                        self.long_live_live[channel] = False
            except Exception as e:
                print("No result {}".format(e))

    def is_stream_live(self, channel):
        return True
        # return self.long_live_live[channel]

    def get_moderators(self, channel):
        moderators = []
        try:
            channel_info_response = requests.get("https://api.twitch.tv/helix/search/channels?query={}".format(channel), headers=self.api_hdrs)
            broadcaster_id = channel_info_response.json()['data'][0]['id']
            headers = copy.deepcopy(self.api_hdrs)
            headers["Authorization"] = "Bearer {}".format(self.streamer_api_tokens[channel])
            resp = requests.get("https://api.twitch.tv/helix/moderation/moderators?broadcaster_id={}".format(broadcaster_id), headers=headers)
            for user in resp.json()['data']:
                #moderators.append(user['user_name'])
                moderators.append(user['user_login'])
        except Exception as e:
            print("Get moderators error {}".format(e))
        print("Twitch Moderators {}".format(str(moderators)))
        return moderators

    @staticmethod
    def anti_bot_check_pass(from_user, message):
        ret_val = False
        if re.match("^.*(wooden|ducky)+.*", message):
            anti.anti_data_handler.register(from_user)
        if anti.anti_data_handler.is_registered(from_user):
            ret_val = True

        # if register failed
        if not ret_val:
            print(f"{from_user} not registered [{message}]")
        return ret_val

    def subscribe_to_streamer_notifications(self, channel):
        channel_info_response = requests.get("https://api.twitch.tv/helix/search/channels?query={}".format(channel),
                                             headers=self.api_hdrs)
        broadcaster_id = channel_info_response.json()['data'][0]['id']
        body = {
            "type": "channel.follow",
            "version": "1",
            "condition": {
                "broadcaster_user_id": broadcaster_id
            },
            "transport": {
                "method": "webhook",
                "callback": "li529-111.members.linode.com/follow_notification",
                "secret": "come55sail88awayy"
            }
        }
        requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", body)
        # gets webhook call back verification pending waiting to confirm callback addr
            # {
            #     "data": [{
            #         "id": "f1c2a387-161a-49f9-a165-0f21d7a4e1c4",
            #         "status": "webhook_callback_verification_pending",
            #         "type": "channel.follow",
            #         "version": "1",
            #         "cost": 1,
            #         "condition": {
            #             "broadcaster_user_id": "12826"
            #         },
            #         "transport": {
            #             "method": "webhook",
            #             "callback": "https://example.com/webhooks/callback"
            #         },
            #         "created_at": "2019-11-16T10:11:12.123Z"
            #     }],
            #     "total": 1,
            #     "total_cost": 1,
            #     "max_total_cost": 10000
            # }
        # twitch calls callback
            #POST https://example.com/webhooks/callback
            # ----
            # Twitch-Eventsub-Message-Id:             e76c6bd4-55c9-4987-8304-da1588d8988b
            # Twitch-Eventsub-Message-Retry:          0
            # Twitch-Eventsub-Message-Type:           webhook_callback_verification
            # Twitch-Eventsub-Message-Signature:      sha256=f56bf6ce06a1adf46fa27831d7d15d
            # Twitch-Eventsub-Message-Timestamp:      2019-11-16T10:11:12.123Z
            # Twitch-Eventsub-Subscription-Type:      channel.follow
            # Twitch-Eventsub-Subscription-Version:   1
            # ----
            # {
            #     "challenge": "pogchamp-kappa-360noscope-vohiyo",
            #     "subscription": {
            #         "id": "f1c2a387-161a-49f9-a165-0f21d7a4e1c4",
            #         "status": "webhook_callback_verification_pending",
            #         "type": "channel.follow",
            #         "version": "1",
            #         "cost": 1,
            #         "condition": {
            #                 "broadcaster_user_id": "12826"
            #         },
            #         "transport": {
            #             "method": "webhook",
            #             "callback": "https://example.com/webhooks/callback"
            #         },
            #         "created_at": "2019-11-16T10:11:12.123Z"
            #     }
            # }
        # Verify the Twitch-Eventsub-Message-Signature header in the callback verification request to make sure the payload came from Twitch. See Verify a signature for more details.
        # Respond to the callback verification request by returning the value of challenge.
        # Your response must be a raw string. If your server is using a web framework, be careful that your web
        # framework isn’t modifying the response in an incompatible way. For example, some web frameworks default to converting responses into JSON objects.

        # When receive on call back verify it was twitch and respond with 200 status code

    def run(self):
        self.subscribe_to_streamer_notifications('woodenducksdontfly')
        self.write_to_system("PASS {}\r\n".format(self.password))
        self.write_to_system("USER {} 0 * {}\r\n".format(self.nickname, self.nickname))
        self.write_to_system("NICK {}\r\n".format(self.nickname))

        print("Connected")
        for channel in self.channels:
            print("Joining {}".format(channel))
            print("[{}]".format(channel))
            self.write_to_system("JOIN #{}\r\n".format(channel))
            print("Joined")
            #TODO on channel update
            self.go_live(self, '', '', channel)
        print("Begin Main Loop")
        #self.write_to_chat(self.greeting)
        # Enter main
        while True:
            received_text = self.irc_channel.receive(1024)
            result = self.pattern.match(received_text)
            if result:
                try:
                    msg_type = result.group(4)
                    if re.match("PRIVMSG ", msg_type):
                        from_user = result.group(2).strip().lower()
                        from_channel = result.group(6).strip().lower()
                        msg_text = result.group(8).strip()
                        message = textutil.sanitize_text(msg_text)
                        if self.penalty_mode == 'disabled' or self.anti_bot_check_pass(from_user, message.lower()):
                            if from_user not in lurk_data.lurk_data_handler.get_lurkers(from_channel):
                                gamble_data.gamble_data_handler.add_recent_chatter(from_user, from_channel)
                            self.message_mailbox.put(("twitch", from_user, message, from_channel))
                        elif self.penalty_mode == 'timeout':
                            self.write_to_chat("/{} {} {}".format(self.penalty_mode,
                                                                  from_user,
                                                                  self.penalty_timeout), from_channel)
                        elif self.penalty_mode == 'ban':
                            self.write_to_chat("/{} {}".format(self.penalty_mode, from_user), from_channel)
                except Exception as err:
                    print("Can't read this {}".format(received_text))
                    print("{}".format(err))
            elif re.match("^PING :(.*)$", received_text):
                self.write_to_system("PONG tmi.twitch.tv\r\n")
