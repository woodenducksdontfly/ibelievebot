import messagehandler


def write_shoutout(bot, shoutout_to, channel):
    bot.write_to_chat("If you're not already following {0}".format(shoutout_to) +
                      " check them out! https://www.twitch.tv/{}".format(shoutout_to), channel)


@messagehandler.register("twitch", "!shoutout")
@messagehandler.register("twitch", "!so")
def shoutout(bot, sent_by, msg_text, channel=None):
    if not messagehandler.is_user_elevated(bot, channel, sent_by):
        return
    try:
        shoutout_to = (msg_text.split(' ')[1]).strip("@")
        write_shoutout(bot, shoutout_to, channel)
    except Exception as e:
        bot.write_to_chat("D: {} got the command wrong!".format(sent_by), channel)


@messagehandler.register("twitch", "!ash")
def chocolatechipcookie15(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        write_shoutout(bot, "chocolatechipcookie15", channel)


@messagehandler.register("twitch", "!jenny")
def justjen(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        write_shoutout(bot, "justjen", channel)


@messagehandler.register("twitch", "!mew")
def mewstache(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        write_shoutout(bot, "mewstache", channel)



@messagehandler.register("twitch", "!silka")
def silkaheart(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        write_shoutout(bot, "silkaheart", channel)


@messagehandler.register("twitch", "!sharky")
def sharky(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        write_shoutout(bot, "mewshark", channel)


@messagehandler.register("twitch", "!firefly")
def firefly(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        write_shoutout(bot, "atomic_fire_fly", channel)



def auto_shoutout(bot, sent_by, msg_text='', channel=None):
    messagehandler.register_timer("twitch", 'auto_so', auto_shoutout, 'woodenducksdontfly', 600.0)
    bot.write_to_chat("Wildhearts stream in mewshark's channel tomorrow evening, be sure to give her a follow https://www.twitch.tv/MewShark", channel)


#messagehandler.register_timer("twitch", 'auto_so', auto_shoutout, 'woodenducksdontfly', 600.0)
