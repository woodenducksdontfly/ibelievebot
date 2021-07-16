import asyncio
import os
import websockets
from bots.bot import Bot
from threading import Thread


global sound_alert_server_instance


# TODO add support for multiple channels
class SoundAlertServer(Thread, Bot):
    def __init__(self, message_mailbox):
        Thread.__init__(self)
        global sound_alert_server_instance
        self.message_mailbox = message_mailbox
        self.websocket = None
        try:
            os.mkdir("static/StreamSounds")
        except FileExistsError as e:
            pass
        sound_alert_server_instance = self

    async def hello(self, websocket, path):
        self.websocket = websocket
        async for message in websocket:
            print(message)
            await self.websocket.send(message)

    async def send_audio(self, filename):
        await self.websocket.send(filename)

    def play_audio(self, bot, from_user, filename, channel):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.send_audio(filename))
        loop.close()

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(self.hello, "localhost", 8085)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
