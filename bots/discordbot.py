import asyncio
from bots.bot import Bot
import discord
from datetime import datetime
from threading import Thread

event_loop = asyncio.get_event_loop()
client = discord.Client()

global discord_bot_instance


@client.event
async def on_ready():
    print("Discord log in complete")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print("[{}] {} - {}: {}".format(datetime.now(), message.channel.id, message.author, message.content))
    discord_bot_instance.message_mailbox.put(("discord", message.author, message.content, str(message.channel.id)))


@client.event
async def on_raw_reaction_add(reaction):
    if reaction.message_id == 786081496187273247:
        guild: discord.Guild = await client.fetch_guild(reaction.guild_id)
        if guild:
            user: discord.Member = await guild.fetch_member(reaction.user_id)
            if user:
                if reaction.emoji.name == "👋":
                    role = discord.utils.get(guild.roles, name="Hello")
                    await reaction.member.add_roles(role)
                elif reaction.emoji.name == "📺":
                    role = discord.utils.get(guild.roles, name="Watch")
                    await reaction.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(reaction):
    if reaction.message_id == 786081496187273247:
        guild: discord.Guild = await client.fetch_guild(reaction.guild_id)
        if guild:
            user: discord.Member = await guild.fetch_member(reaction.user_id)
            if user:
                if reaction.emoji.name == "👋":
                    role = discord.utils.get(guild.roles, name="Hello")
                    await user.remove_roles(role)
                elif reaction.emoji.name == "📺":
                    role = discord.utils.get(guild.roles, name="Watch")
                    await user.remove_roles(role)


class DiscordBot(Thread, Bot):
    def __init__(self, discord_token, message_mailbox):
        Thread.__init__(self)
        global discord_bot_instance
        self.discord_token = discord_token
        self.message_mailbox = message_mailbox

        discord_bot_instance = self

    async def message_process(self, channel, message):
        my_channel: discord.TextChannel = client.get_channel(int(channel))
        await my_channel.send(str(message))

    def write_to_chat(self, message, channel=None):
        while not client.is_ready():
            # Wait for discord client to be ready to receive messages
            pass
        print("[{}] {} - ibelivebot#8397: {}".format(datetime.now(), channel, message))
        event_loop.create_task(self.message_process(channel, message))

    def run(self):
        event_loop.create_task(client.start(self.discord_token))
        event_loop.run_forever()

