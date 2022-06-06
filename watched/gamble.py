import math
import messagehandler
from data_handlers import user_data, gamble_data
import random
import re
import requests
import inspect
import cooldown

currency = "waffles"
combo_currency = "jugs of syrup"
invalid_users = ["local.mockuser",
                 "communityshowcase",
                 "nightbot",
                 "streamelements",
                 "ibelievebot",
                 "commanderroot",
                 "rubberslayer",
                 "letsdothis_hostraffle",
                 "nightbot",
                 "lurxx",
                 "anotherttvviewer",
                 "soundalerts",
                 "discord_for_streamers",
                 "mslenity",
                 "d1sc0rdforsmallstreamers",
                 "bingcortana",
                 "SoundAlerts",
                 "sad_grl",
                 "dankingaround",
                 "woodenducksdontfly"]

global appeal_for_syrup
appeal_for_syrup = []


def get_valid_players(channel, viewers, vips, mods):
    players = [viewer.lower() for viewer in viewers] + \
               [vip.lower() for vip in vips] + \
               [mod.lower() for mod in mods]
    the_best = list(filter(lambda i: i not in invalid_users, players))
    return the_best


def _give_everyone_currency(bot, sent_by, msg_txt, channel):
    messagehandler.register_timer("twitch", 'currency_handout_{}'.format(channel), _give_everyone_currency, channel, 600.0)
    if bot.is_stream_live(channel):
        # TODO update channel
        response = requests.get('http://tmi.twitch.tv/group/user/{}/chatters'.format(channel))
        if response.status_code == 200:
            chatters = response.json()['chatters']
            viewers = chatters.get('viewers', {})
            vips = chatters.get('vips', {})
            mods = chatters.get('moderators', {})
            currency_payout = random.randint(10, 300)
            calling = True

            for player in get_valid_players(channel, viewers, vips, mods):
                if player.lower() in get_valid_players(channel, viewers, vips, mods):
                    if calling:
                        bot.write_to_chat('{} delivery, all chatters get {} {}'.format(currency.upper()[:-1],
                                                                                          currency_payout,
                                                                                          currency),
                                          channel)
                        calling = False
                    user_data.user_data_handler.add_balance_wait_for_flush(player, currency_payout)
            user_data.user_data_handler.flush_data()
        else:
            print("tmi api disappeared")


def _give_everyone_syrup(bot, sent_by, msg_txt, channel):
    messagehandler.register_timer("twitch", 'syrup_handout_{}'.format(channel), _give_everyone_syrup, channel, 600.0)
    if bot.is_stream_live(channel):
        # TODO update channel
        response = requests.get('http://tmi.twitch.tv/group/user/{}/chatters'.format(channel))
        if response.status_code == 200:
            chatters = response.json()['chatters']
            viewers = chatters.get('viewers', {})
            vips = chatters.get('vips', {})
            mods = chatters.get('moderators', {})
            currency_payout = random.randint(2, 50)
            calling = True

            valid_players = get_valid_players(channel, viewers, vips, mods)
            bonus_syrup_user = None
            if len(valid_players) > 0:
                bonus_syrup_user = valid_players[(random.randint(0, len(valid_players)-1))].lower()
            for player in valid_players:
                if player.lower() in get_valid_players(channel, viewers, vips, mods):
                    if calling:
                        bot.write_to_chat('Sweet sweet {} all chatters get {} {}'.format(combo_currency.upper(),
                                                                                         currency_payout,
                                                                                         combo_currency),
                                          channel)
                        calling = False
                    user_data.user_data_handler.add_syrup_balance_wait_for_flush(player, currency_payout)
            if bonus_syrup_user:
                user_data.user_data_handler.add_syrup_balance_wait_for_flush(bonus_syrup_user, 5)
                if bonus_syrup_user not in gamble_data.gamble_data_handler.get_recent_chatters(channel):
                    print("Secret syrup payout to {}".format(bonus_syrup_user))
                    bonus_syrup_user = "someone lurking"
                bot.write_to_chat(f'The tree lords are particularly fond of {bonus_syrup_user}' +
                                  f' and have rewarded them with 5 bonus {combo_currency}',
                                  channel)
            user_data.user_data_handler.flush_data()
        else:
            print("tmi api disappeared")


@messagehandler.register("twitch", "!appeal")
def syrup_appeal(bot, sent_by, msg_text, channel=None):
    global appeal_for_syrup
    if sent_by.lower() not in appeal_for_syrup:
        appeal_for_syrup.append(sent_by.lower())
        bot.write_to_chat("The tree lords will think about your request {}".format(sent_by), channel)
    if not bot.timers.get("syrup_appeal_{}".format(channel)):
        messagehandler.register_timer("twitch", 'syrup_appeal_{}'.format(channel), _answer_syrup_appeal, channel, 300.0)


def _answer_syrup_appeal(bot, sent_by, msg_text, channel=None):
    global appeal_for_syrup
    winner = bool(random.randint(10, 100) >= 50)
    if winner:
        currency_payout = random.randint(2, 10)
        for player in appeal_for_syrup:
            user_data.user_data_handler.add_syrup_balance_wait_for_flush(player, currency_payout)
        user_data.user_data_handler.flush_data()
        bot.write_to_chat("Everyone who has asked for syrup has received {} {}".format(currency_payout, combo_currency),
                          channel)
    else:
        bot.write_to_chat("The tree lords have denied everyone's request for more {}".format(combo_currency),
                          channel)
    appeal_for_syrup = []


@messagehandler.register("twitch", "!roll")
@messagehandler.register("twitch", "!chance")
def roll(bot, sent_by, msg_text, channel=None):
    if gamble_data.gamble_data_handler.is_valid_roll(sent_by, channel):
        reward = random.randint(10, 250)
        user_data.user_data_handler.add_syrup_balance(sent_by, reward)
        bonus_msg = "" if reward < 100 else " Good Roll!!!"
        bot.write_to_chat("{} has been awarded {} {}{}".format(sent_by, reward, combo_currency, bonus_msg), channel)


# TODO clean this garbage up
@messagehandler.register("twitch", "!bet")
@messagehandler.register("twitch", "!gamble")
def gamble(bot, sent_by, msg_text, channel=None):
    function_name = inspect.stack()[1][3]
    in_cooldown = cooldown.cooldown(function=function_name,
                                    number_of_calls=10,
                                    within_timelimit=15,
                                    cooldown_for_time=150)
    if in_cooldown:
        if not cooldown.is_cooldown_message_sent(function_name):
            bot.write_to_chat("Gambling is in cooldown, please don't spam chat", channel)
            cooldown.set_cooldown_message_sent(function_name)
        return

    if not bot.is_stream_live(channel):
        return
    try:
        club_status = user_data.user_data_handler.get_club_status(sent_by)
        if club_status:
            if club_status == "God":
                bot.write_to_chat("Please Gods have no need to gamble", channel)
                return
        try:
            msg_text = re.sub("\s+", " ", msg_text)
            amount_to_gamble = int(msg_text.split(' ')[1])
            my_balance = user_data.user_data_handler.get_balance(sent_by)
        except Exception as ea:
            try:
                my_balance = user_data.user_data_handler.get_balance(sent_by)
                if msg_text.split(' ')[1] == "all":
                    if my_balance <= 0:
                        bot.write_to_chat("All of what!", channel)
                        return
                    amount_to_gamble = user_data.user_data_handler.get_balance(sent_by)
                elif msg_text.split(' ')[1] == "half":
                    if my_balance > 2:
                        amount_to_gamble = math.floor(my_balance / 2)
                    else:
                        bot.write_to_chat("You need more {}".format(currency), channel)
                elif msg_text.split(' ')[1] == "most":
                    if my_balance > 2:
                        amount_to_gamble = math.floor(my_balance * 0.7)
                    else:
                        bot.write_to_chat("You need more {}".format(currency), channel)
                elif msg_text.split(' ')[1] == "some":
                    if my_balance > 2:
                        amount_to_gamble = math.floor(my_balance * 0.3)
                    else:
                        bot.write_to_chat("You need more {}".format(currency), channel)
                else:
                    bot.write_to_chat("I'll gamble your {}".format(msg_text.split(' ')[1]), channel)
                    return
            except Exception as eb:
                print(eb)
                raise eb
        if amount_to_gamble < 0:
            bot.write_to_chat("Seriously? More debt?", channel)
            return

        if my_balance <= 0 and amount_to_gamble > 100:
            bot.write_to_chat("Hold up, you're in debt," +
                              f" I'm limiting you to 100 {currency} per bet until you're out",
                              channel)
            return

        if user_data.user_data_handler.get_club_status(sent_by):
            modifier = (user_data.user_data_handler.get_golden_waffles() * 5)
        else:
            modifier = 0

        lost = bool(random.randint(0, 100) < (40 + modifier))

        if lost:
            user_data.user_data_handler.subtract_balance(sent_by, amount_to_gamble)
            bot.write_to_chat('{0} lost {1} {3} and now has {2} {3}'.format(sent_by,
                                                                            amount_to_gamble,
                                                                            user_data.user_data_handler.get_balance(sent_by),
                                                                            currency),
                                                                            channel)
        else:
            user_data.user_data_handler.add_balance(sent_by, amount_to_gamble)
            bot.write_to_chat('{0} won {1} {3} and now has {2} {3}'.format(sent_by,
                                                                           amount_to_gamble,
                                                                           user_data.user_data_handler.get_balance(sent_by),
                                                                           currency),
                                                                           channel)
    except SyntaxError:
        pass
    except IndexError:
        bot.write_to_chat('No')


@messagehandler.register("twitch", "!stock")
@messagehandler.register("twitch", "!stack")
@messagehandler.register("twitch", "!balance")
@messagehandler.register("twitch", "!points")
@messagehandler.register("twitch", "!waffles")
@messagehandler.register("twitch", "!waffle")
@messagehandler.register("twitch", "!syrup")
@messagehandler.register("twitch", "!syurp")
@messagehandler.register("twitch", "!seerup")
@messagehandler.register("twitch", "!surup")
@messagehandler.register("twitch", "!szurup")
@messagehandler.register("twitch", "!jugs")
@messagehandler.register("twitch", "!!cerialup")
def balance(bot, sent_by, msg_text, channel=None):
    try:
        my_balance = user_data.user_data_handler.get_balance(sent_by)
        my_syrup_balance = user_data.user_data_handler.get_syrup_balance(sent_by)
        my_golden_waffle_balance = user_data.user_data_handler.get_golden_waffles(sent_by)
        golden_balance_text = ""
        if my_golden_waffle_balance:
            if my_golden_waffle_balance > 0:
                golden_balance_text = f"{my_golden_waffle_balance} Golden Waffles "
        bot.write_to_chat('{} has {}{} {} and {} {}'.format(sent_by,
                                                          golden_balance_text,
                                                          my_balance,
                                                          currency,
                                                          my_syrup_balance,
                                                          combo_currency), channel)
    except Exception as e:
        pass


@messagehandler.register("twitch", "!give")
def give(bot, sent_by, msg_text, channel=None):
    try:
        who_to_give = msg_text.split(' ')[1].lower()
    except Exception as e:
        print("WHO")
        return
    try:
        amount_to_give = int(msg_text.split(' ')[2])
    except Exception as e:
        print("NAN")
        return
    if abs(amount_to_give) != amount_to_give:
        return
    if user_data.user_date_handler.get_club_status(sent_by) == "God":
        return
    if sent_by != "woodenducksdontfly" and sent_by != "local.MockUser":
        user_data.user_data_handler.add_balance(who_to_give, amount_to_give)
    elif user_data.user_data_handler.get_balance(sent_by) >= abs(amount_to_give):
        user_data.user_data_handler.subtract_balance(sent_by, amount_to_give)
        user_data.user_data_handler.add_balance(who_to_give, amount_to_give)
    bot.write_to_chat('Gave {} {} {}'.format(who_to_give, amount_to_give, currency), channel)


@messagehandler.register("twitch", "!top5")
def top_five(bot, sent_by, msg_text, channel=None):
    users = user_data.user_data_handler.get_top_users_by_balance()
    output = ""
    for rank, user in enumerate([user for user in users if user not in invalid_users][:5]):
        output += "{}. {}: {} ".format(rank+1, user, user_data.user_data_handler.get_balance(user))
    bot.write_to_chat(output, channel)


@messagehandler.register("twitch", "!syrup5")
@messagehandler.register("twitch", "!seerup5")
def top_syrup_five(bot, sent_by, msg_text, channel=None):
    users = user_data.user_data_handler.get_top_syrup_users_by_balance()
    output = ""
    for rank, user in enumerate([user for user in users if user not in invalid_users][:5]):
        output += "{}. {}: {} ".format(rank+1, user, user_data.user_data_handler.get_syrup_balance(user))

    bot.write_to_chat(output, channel)


@messagehandler.register("twitch", "!bottom5")
def bottom_five(bot, sent_by, msg_text, channel=None):
    users = user_data.user_data_handler.get_bottom_users_by_balance()
    output = "O_O I'm NOT targeting you "
    for rank, user in enumerate([user for user in users if user not in invalid_users][:5]):
        output += "{}. {}: {} ".format(rank+1, user, user_data.user_data_handler.get_balance(user))
    bot.write_to_chat(output, channel)


@messagehandler.register("twitch", "!wealthy")
def club(bot, sent_by, msg_text, channel=None):
     bot.write_to_chat("Coming soon :)", channel)
     #TODO list users by level
#     club_status = user_data.user_data_handler.get_club_status(sent_by)
#     output = ""
#     if club_status:
#         if club_status is int:
#             output = "{} has {} golden waffles".format(sent_by, club_status)
#         else:
#             if club_status == "revoked":
#                 output = "Hows it feel loosing all the loot @{}".format(sent_by)
#             elif club_status == "God":
#                 output = "All praise {}".format(sent_by)
#
#     else:
#         output = "{} has no golden waffles".format(sent_by)
#      bot.write_to_chat(output, channel)
#
#


@messagehandler.register("twitch", "!club")
def club_rank(bot, sent_by, msg_text, channel=None):
    #TODO Cooldown
    club_status = user_data.user_data_handler.get_club_status(sent_by)
    if club_status:
        bot.write_to_chat(club_status, channel)
    else:
        bot.write_to_chat("Maybe one day")


@messagehandler.register("twitch", "!buy")
def buy(bot, sent_by, msg_text, channel=None):
    club_status = user_data.user_data_handler.get_club_status(sent_by)
    output = ""
    if club_status != "God":
        previous_club_status = user_data.user_data_handler.get_club_status(sent_by)
        user_data.user_data_handler.add_gold_waffles(sent_by)
        club_status = user_data.user_data_handler.get_club_status(sent_by)
        if club_status == "God" or previous_club_status:
            output = f"{sent_by} is now a {currency} {club_status}"
        else:
            output = f"New Member! {sent_by} is now a {club_status}"
    else:
        output = "Ha please, you don't need more waffles"

    bot.write_to_chat(output, channel)


@messagehandler.register("twitch", "!sell")
def sell(bot, sent_by, msg_text, channel=None):
    club_status = user_data.user_data_handler.get_club_status(sent_by)
    output = ""
    if club_status != "God" and user_data.user_data_handler.get_golden_waffles(sent_by) > 0:
        previous_club_status = user_data.user_data_handler.get_club_status()
        user_data.user_data_handler.remove_gold_waffle(sent_by)
        club_status = user_data.user_data_handler.get_club_status()
        if club_status:
            output = f"{sent_by} is now a {currency} {club_status}"
        else:
            output = "You're too poor now :p"
    else:
        output = "You know I can't allow that"
    bot.write_to_chat(output, channel)


@messagehandler.register("twitch", "!eat")
@messagehandler.register("discord", "!eat")
def eat(bot, sent_by, msg_text, channel=None):
    function_name = inspect.stack()[1][3]
    in_cooldown = cooldown.cooldown(function=function_name,
                                    number_of_calls=10,
                                    within_timelimit=15,
                                    cooldown_for_time=150)
    if in_cooldown:
        if not cooldown.is_cooldown_message_sent(function_name):
            bot.write_to_chat("Gambling is in cooldown, please don't spam chat", channel)
            cooldown.set_cooldown_message_sent(function_name)
        return
    # TODO tie twitch username to discord name
    amount_to_eat = 1
    try:
        msg_text = re.sub("\s+", " ", msg_text)
        amount_to_eat = int(msg_text.split(' ')[1])
        if amount_to_eat <= 0:
            amount_to_eat = 1
        elif amount_to_eat > user_data.user_data_handler.get_balance(sent_by):
            bot.write_to_chat('{0} thinks they have more waffles than they do'.format(sent_by), channel)
            amount_to_eat = 1
    except Exception as ea:
        pass
    user_data.user_data_handler.subtract_balance(sent_by, amount_to_eat)
    bot.write_to_chat('{0} has eaten {1} waffle(s) from their stock'.format(sent_by, amount_to_eat), channel)


@messagehandler.register("twitch", "!chug")
def chug(bot, sent_by, msg_text, channel=None):
    amount_to_drink = 1
    user_data.user_data_handler.subtract_syrup_balance(sent_by, amount_to_drink)
    bot.write_to_chat('{0} has chugged a jug of syrup from their stock'.format(sent_by, amount_to_drink), channel)


@messagehandler.register("twitch", "!dine")
def chug(bot, sent_by, msg_text, channel=None):
    amount = 1
    user_data.user_data_handler.subtract_syrup_balance(sent_by, amount)
    user_data.user_data_handler.subtract_balance(sent_by, amount)
    bot.write_to_chat('{0} has enjoyed a syrup coated waffle'.format(sent_by, amount), channel)

@messagehandler.register("twitch", '!mk')
def mk(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat("mini 1542-7514-2187", channel)

@messagehandler.register("twitch", "!quaskyisadirtycheaterandhasnoshame")
def quaskyisadirtycheaterandhasnoshame(bot, sent_by, msg_text, channel=None):
    if sent_by != "quasky" and sent_by != "local.MockUser":
        bot.write_to_chat('only quasky can cheat you silly bean', channel)
        return
    else:
        user_data.user_data_handler.add_balance(sent_by, 999999999999999999999999999999999999999999)


