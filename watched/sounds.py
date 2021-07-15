import messagehandler
from file_handler import user_data


def _use_points(user):
    if user_data.user_data_handler.get_syrup_balance(user) >= 10:
        user_data.user_data_handler.subtract_syrup_balance(user, 10)
        return True
    else:
        return False


@messagehandler.register("twitch", "!wow")
def wow(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'anime-wow-sound-effect-mp3cut.mp3', channel))


@messagehandler.register("twitch", "!poyo")
def poyo(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'kirby-poyo.mp3', channel))


@messagehandler.register("twitch", "!smash")
def smash(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'lemme-smash.mp3', channel))


@messagehandler.register("twitch", "!get")
def get(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'Obtain_Fanfare.mp3', channel))


@messagehandler.register("twitch", "!sheesh")
def sheesh(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'SHEESH SOUND EFFECT.mp3', channel))


@messagehandler.register("twitch", "!birthday")
def birthday(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'thor-ragnarok-its-my-birthday-scene-hd-audiotrimmer.mp3', channel))


@messagehandler.register("twitch", "!wah")
def wah(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'waluigi_wahring2mob.mp3', channel))


@messagehandler.register("twitch", "!no")
def no(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'no.mp3', channel))


@messagehandler.register("twitch", "!yes")
def yes(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'yes.mp3', channel))


@messagehandler.register("twitch", "!nut")
def nut(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'nut.mp3', channel))


@messagehandler.register("twitch", "!owo")
def owo(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'owo.wav', channel))


@messagehandler.register("twitch", "!uwu")
def uwu(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'uwu.mp3', channel))


@messagehandler.register("twitch", "!bwoop")
def bwoop(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'owo_uwu.mp3', channel))


@messagehandler.register("twitch", "!quasky")
def quasky(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'TrueFeelingsNoBackgroundLowerVolume.mp3', channel))


@messagehandler.register("twitch", "!skeletons")
def skeletons(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'spooky-scary-skeleton_WnTSX24(1).mp3', channel))


@messagehandler.register("twitch", "!quack")
def skeletons(bot, sent_by, msg_text, channel=None):
    if _use_points(sent_by):
        bot.message_mailbox.put(("audio", sent_by, 'Quack.wav', channel))
