import messagehandler


@messagehandler.register("twitch", "!poke")
@messagehandler.register("twitch", "!stab")
@messagehandler.register("twitch", "!fuck")
def stab(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("That's lewd @{}".format(sent_by), channel)


@messagehandler.register("twitch", "!attack")
def attack(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("Woah now @{} let's think about that".format(sent_by), channel)


@messagehandler.register("twitch", "!duel")
def duel(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("Take the fight outside @{}".format(sent_by), channel)


@messagehandler.register("twitch", "!assassinate")
@messagehandler.register("twitch", "!asasinate")
@messagehandler.register("twitch", "!asassinate")
@messagehandler.register("twitch", "!assasinate")
def assassinate(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("Well that's just rude @{}".format(sent_by), channel)


@messagehandler.register("twitch", "!bully")
@messagehandler.register("twitch", "!booli")
def bully(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("No booli!!", channel)
