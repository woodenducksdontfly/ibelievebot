import messagehandler


current_game = "Trials of Mana"


@messagehandler.register("twitch", '!day1')
def day_one(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("D1 {}: We selected Duran, Angela, and Charlotte. Next thing you know, a quest was thrust upon us".format(current_game), channel)


@messagehandler.register("twitch", '!day2')
def day_two(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("D2 {}: We collected gnome. Not much else :)".format(current_game), channel)


@messagehandler.register("twitch", '!day3')
def day_three(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("D3 {}: We went back home and found Angela's homeland attacking us".format(current_game), channel)


@messagehandler.register("twitch", '!day4')
def day_four(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("D4 {}: We talked about wind but only found some Koropokkurs".format(current_game), channel)


@messagehandler.register("twitch", '!day5')
def day_five(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("D5 {}: We finally found the wind elemental and changed our classes (D:Light, A:Dark, C:Light)".format(current_game), channel)


@messagehandler.register("twitch", '!day6')
def day_six(bot, sent_by, msg_text, channel=None):
    # hdmi adapter futzed bad
    bot.write_to_chat("D6 {}: Botched the recording so starting over tomorrow".format(current_game), channel)


@messagehandler.register("twitch", '!day7')
def day_six(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("D7 {}: We retook Laurent, survived a ghost ship, got the darkness elemental, and obtained a fairy flute, oh and we met evil babe and dude".format(current_game), channel)


@messagehandler.register("twitch", '!day8')
def day_eight(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("We got Salamando and rescued a princess!", channel)


@messagehandler.register("twitch", '!day9')
def day_nine(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("Two Elementals in one day! We now have Undine and Luna", channel)


@messagehandler.register("twitch", '!day10')
def day_ten(bot, sent_by, msg_text, channel=None):
    # Lets take Lampbloom Woods
    bot.write_to_chat("We have all the elementals and became friends with Flamie! Angela's mother has been captured? Gasp!", channel)


@messagehandler.register("twitch", '!day11')
def day_eleven(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("We beat up some benevodons, I can't tell if I'm under or over leveled", channel)


@messagehandler.register("twitch", '!day12')
def day_twelve(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("Coming Soon", channel)

