import argparse
from datetime import datetime

import bots.twitchbot
import bots.discordbot
import bots.soundalertserver
from queue import Queue
from flask import Flask, make_response, send_file, send_from_directory, request
from data_handlers import anti, gamble_data, lurk_data, static, user_data, stream
import messagehandler
import customlogger
import logging
import os
import json
from pprint import pprint

app = Flask(__name__)
twitch_bot = None
twitter_bot = None
youtube_bot = None
slack_bot = None
discord_bot = None


@app.route('/')
def root_page(self):
    # TODO webui control
    return 'Authenticate & controller program'


@app.route('/audio')
def audio_page():
    resp = make_response(send_file('static/audio.html'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Feature-Policy'] = "autoplay '*'"
    return resp


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/get_audio/<path:path>')
def get_audio(path):
    return send_from_directory('static/StreamSounds', path)


@app.route('/follow_notification', methods=['POST'])
def endpoint():
    pprint(request.data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/channels')
def channels():
    resp = ""
    with open('data/join_channels.json', 'r') as join_channels:
        for channel in json.load(join_channels):
            resp = channel
    return resp


if __name__ == "__main__":
    logger = customlogger.get_logger(__name__)
    logger.log(logging.INFO, f" {'='*40} Bot  Start {'='*40} ")
    logger.log(logging.INFO, f" {'='*32} {datetime.now()} {'='*32} ")
    # logger.log(logging.INFO, f" {'='*92} ")
    parser = argparse.ArgumentParser()
    parser.add_argument('--mock', action="store_true")
    parser.add_argument('--no-auto', action="store_false", dest='auto_start')
    parser.add_argument('--no-go-live-notification', action="store_false", default="store_true", dest='go_live_notification')
    args = parser.parse_args()

    message_mailbox = Queue()
    stream_info = {'is_live', False}
    # Define secrets to avoid interpreter warnings
    streamer = None  # Secret
    channel = None  # Secret
    twitch_client_id = None  # Secret
    twitch_oauth = None  # Secret
    twitch_api_oauth = None  # Secret
    discord_token = None  # Secret
    slack_token = None  # Secret
    youtube_token = None  # Secret
    # Read in secrets
    try:
        with open("data/secrets.py") as f:
            exec(f.read())
    except FileNotFoundError:
        try:
            os.mkdir("data")
        except FileExistsError as e:
            pass
        # with open("data/secrets.py", 'w') as f:
        #     f.write('streamer = "woodenducksdontfly"\n')
        #     f.write('channel = streamer\n')
        #     f.write('twitch_client_id = ""\n')
        #     f.write('twitch_oauth = "oauth:"\n')
        #     f.write('twitch_api_oauth = ""\n')
        #     f.write('discord_token = ""\n')
        #     f.write('slack_token = ""\n')
        #     f.write('youtube_token = ""\n')
        # print("Update data/secrets.py")
        exit()

    anti.AntiDataHandler()
    gamble_data.GambleDataHandler()
    lurk_data.LurkDataHandler()
    user_data.UserDataHandler()
    static.StaticFileHandler()
    stream.StreamDataHandler()
    message_handler = messagehandler.MessageHandler(message_mailbox)

    twitch_bot = bots.twitchbot.TwitchBot(streamer,
                                          twitch_client_id,
                                          twitch_oauth,
                                          twitch_api_oauth,
                                          message_mailbox,
                                          mock_irc=args.mock,
                                          go_live_notification=args.go_live_notification)
    discord_bot = bots.discordbot.DiscordBot(discord_token, message_mailbox)
    # slack_bot = bots.slackbot.SlackBot(slack_token, message_mailbox)
    sound_alert_server = bots.soundalertserver.SoundAlertServer(message_mailbox)

    message_handler.register_bot("twitch", twitch_bot)
    message_handler.register_bot("discord", discord_bot)
    message_handler.register_bot("audio", sound_alert_server)
    message_handler.start()

    # Need to let gil run because of multithreading
    while not message_handler.ready:
        pass
    if args.auto_start:
        twitch_bot.start()
        discord_bot.start()
        sound_alert_server.start()
    app.run()
    message_handler.join()
    twitch_bot.join()
    discord_bot.join()
    sound_alert_server.join()
    print("Shutdown successful")

