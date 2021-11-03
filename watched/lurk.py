import messagehandler
from data_handlers import gamble_data, lurk_data


@messagehandler.register("twitch", "!blurk")
def blurk(bot, sent_by, msg_text, channel=None):
    if sent_by not in lurk_data.lurk_data_handler.get_lurkers(channel):
        bot.write_to_chat("oh heck we got a blurker, we're gonna just send you off to lurk city", channel)
    lurk(bot, sent_by, msg_text)
    gamble_data.gamble_data_handler.remove_recent_chatter(sent_by, channel)


@messagehandler.register("twitch", "!lurk")
def lurk(bot, sent_by, msg_text, channel=None):
    lurkers = lurk_data.lurk_data_handler.get_lurkers(channel)
    if sent_by not in lurkers:
        if len(lurkers) > 1:
            bot.write_to_chat("{} has joined the others in lurk city.".format(sent_by), channel)
        elif len(lurkers) == 1:
            flattened_lurkers = " ".join(list(lurkers))
            bot.write_to_chat(f"{sent_by} has joined {flattened_lurkers} in lurk city.", channel)
        else:
            bot.write_to_chat("{} is off to lurk city alone".format(sent_by), channel)
        lurk_data.lurk_data_handler.add_lurker(channel, sent_by)
        gamble_data.gamble_data_handler.remove_recent_chatter(sent_by, channel)
    else:
        bot.write_to_chat("{} is already in lurk city".format(sent_by), channel)


@messagehandler.register("twitch", "!unlurk")
@messagehandler.register("twitch", "!nolurk")
@messagehandler.register("twitch", "!notlurk")
def unlurk(bot, sent_by, msg_text, channel=None):
    if sent_by in lurk_data.lurk_data_handler.get_lurkers(channel):
        lurk_data.lurk_data_handler.remove_lurker(channel, sent_by)
        gamble_data.gamble_data_handler.add_recent_chatter(sent_by, channel)
        bot.write_to_chat("{} has returned from lurk city".format(sent_by), channel)
    else:
        bot.write_to_chat("{} never made it to lurk city".format(sent_by), channel)


@messagehandler.register("twitch", "!lurkpop")
def lurkpop(bot, sent_by, msg_text, channel=None):
    lurkers = lurk_data.lurk_data_handler.get_lurkers(channel)
    if len(lurkers) >= 1:
        flattened_lurkers = " ".join(list(lurk_data.lurk_data_handler.get_lurkers(channel)))
        bot.write_to_chat("Population: {}, Current residents: {}".format(len(lurkers), flattened_lurkers), channel)
    else:
        bot.write_to_chat("Lurk city is a ghost town", channel)
