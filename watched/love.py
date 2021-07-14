import messagehandler
import numpy
from better_profanity import profanity


@messagehandler.register("twitch", "!love")
def love(bot, sent_by, msg_text, channel=None):
    try:
        if profanity.contains_profanity(msg_text):
            return
        extra_command = msg_text.split(' ', 1)[1]
        v = numpy.random.default_rng().exponential(10)
        if v < 0:
            print("HALP NEGATIVE")
            print(v)
        love_percent = round(numpy.maximum(50, 100 - v), 2)
        bot.write_to_chat('There is {}% love between {} and {}'.format(love_percent, sent_by, extra_command), channel)
    except IndexError:
        pass


@messagehandler.register("twitch", "!hug")
def hug(bot, sent_by, msg_text, channel=None):
    try:
        if profanity.contains_profanity(msg_text):
            return
        extra_command = msg_text.split(' ', 1)[1]
        bot.write_to_chat('@{} you get a hug'.format(extra_command), channel)
    except IndexError:
        pass
