import messagehandler


lurkers = set()


@messagehandler.register("twitch", "!blurk")
def blurk(bot, sent_by, msg_text, channel=None):
    if sent_by not in lurkers:
        bot.write_to_chat("oh heck we got a blurker, we're gonna just send you off to lurk city", channel)
    lurk(bot, sent_by, msg_text)


@messagehandler.register("twitch", "!lurk")
def lurk(bot, sent_by, msg_text, channel=None):
    if sent_by not in lurkers:
        if len(lurkers) > 1:
            bot.write_to_chat("{} has joined the others in lurk city.".format(sent_by), channel)
        elif len(lurkers) == 1:
            bot.write_to_chat("{} has joined {} in lurk city.".format(sent_by, " ".join(list(lurkers))), channel)
        else:
            bot.write_to_chat("{} is off to lurk city alone".format(sent_by), channel)
        lurkers.add(sent_by)
    else:
        bot.write_to_chat("{} is already in lurk city".format(sent_by), channel)


@messagehandler.register("twitch", "!unlurk")
@messagehandler.register("twitch", "!nolurk")
@messagehandler.register("twitch", "!notlurk")
def unlurk(bot, sent_by, msg_text, channel=None):
    if sent_by in lurkers:
        lurkers.remove(sent_by)
        bot.write_to_chat("{} has returned from lurk city".format(sent_by), channel)
    else:
        bot.write_to_chat("{} never made it to lurk city".format(sent_by), channel)


@messagehandler.register("twitch", "!lurkpop")
def lurkpop(bot, sent_by, msg_text, channel=None):
    if len(lurkers) >= 1:
        bot.write_to_chat("Population: {}, Current residents: {}".format(len(lurkers), " ".join(list(lurkers))), channel)
    else:
        bot.write_to_chat("Lurk city is a ghost town", channel)
