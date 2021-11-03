import messagehandler
import random
import re
from datetime import datetime


@messagehandler.register("twitch", "!believe")
def believe(bot, sent_by, msg_text, channel=None):
    believes = ["You gotta believe!",
                "Beeeelieve it!",
                "Your potential self is infinite!",
                "Believe in the me that believes in you!",
                "Believe in the tree lords again"]
    bot.write_to_chat(random.choice(believes), channel)


@messagehandler.register("twitch", "!hullo")
def hullo(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("Hullo!! Hi! Hello!!!", channel)


@messagehandler.register("twitch", "!discord")
def discord(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("https://discord.gg/Xmf2YaK", channel)


@messagehandler.register("twitch", "!socials")
def socials(bot, sent_by, msg_text, channel=None):
    discord(bot, sent_by, msg_text)


@messagehandler.register("twitch", "!ellipses")
@messagehandler.register("twitch", "!...")
def ellipses(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("...", channel)


@messagehandler.register("twitch", "^")
def carrot(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("^", channel)


@messagehandler.register("twitch", "same")
def same(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("same", channel)


@messagehandler.register("twitch", "!covid")
def covid(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("https://coronavirus.jhu.edu/map.html", channel)


@messagehandler.register("twitch", '!firstplay')
def blind(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("It means I've never played it.  Plz no spoilers.", channel)


@messagehandler.register("twitch", '!3pm')
def three_pm(bot, sent_by, msg_text, channel=None):
    now = datetime.now()
    today3pm = now.replace(hour=15, minute=0, second=0, microsecond=0)
    if now >= today3pm:
        bot.write_to_chat("It's fine I can wear shorts, shorts are allowed", channel)
    else:
        bot.write_to_chat("Please don't tell anyone I'm wearing shorts", channel)


@messagehandler.register("twitch", '!YOLT')
def yolt(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("You Only Live Twice!", channel)


@messagehandler.register("twitch", '!YODO')
def yodo(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("You Only Die Once!", channel)


@messagehandler.register("twitch", '!blame')
def blame(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("{} has blamed {} for this occurrence".format(sent_by, msg_text), channel)

@messagehandler.register("twitch", '!chess')
def blame(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("https://www.chess.com/member/woodenduck", channel)

@messagehandler.register("twitch", '!src')
def blame(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("https://github.com/woodenducksdontfly/ibelievebot", channel)

@messagehandler.register("twitch", '!hammer')
def hammer(bot, sent_by, msg_text, channel=None):
    if not messagehandler.is_user_elevated(bot, channel, sent_by):
        return
    bot.penalty_mode = 'ban'
    print("======================== Hammer Mode {} ========================".format(bot.penalty_mode))

@messagehandler.register("twitch", '!stick')
def stick(bot, sent_by, msg_text, channel=None):
    if not messagehandler.is_user_elevated(bot, channel, sent_by):
        return
    timeout_in_seconds = 5
    try:
        msg_text = re.sub("\s+", " ", msg_text)
        timeout_in_seconds = max(int(msg_text.split(' ')[1]), 5)
    except Exception as ea:
        pass
    bot.penalty_mode = 'timeout'
    bot.penalty_timeout = timeout_in_seconds
    print("======================== Stick Mode {} - {} ========================".format(bot.penalty_mode,
                                                                                        bot.penalty_timeout))


@messagehandler.register("twitch", '!rollwithus')
def blame(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("!play", channel)


# TODO this needs work
@messagehandler.register("twitch", '!welcome')
def blame(bot, sent_by, msg_text, channel=None):
    if not messagehandler.is_user_elevated(bot, channel, sent_by):
        return
    username = "everyone"
    try:
        username = re.sub("\s+", " ", msg_text).split(' ')[1]
    except Exception as ea:
        # previous user should be added to user_registry
        pass
    bot.write_to_chat(f"Welcome {username} you can chat now :)!", channel)
