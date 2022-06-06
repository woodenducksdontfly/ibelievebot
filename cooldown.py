import uuid
from threading import Timer
from utils.expiringdict import ExpiringDict


cooldown_monitor = {}


def out_of_cooldown_callback(function):
    cooldown_monitor[function]['in_cooldown'] = False
    cooldown_monitor[function]['cooldown_message_sent'] = False


def is_cooldown_message_sent(function):
    if cooldown_monitor.get(function):
        return cooldown_monitor[function]['cooldown_message_sent']
    else:
        return False


def set_cooldown_message_sent(function):
    cooldown_monitor[function]['cooldown_message_sent'] = True


def cooldown(function, number_of_calls, within_timelimit, cooldown_for_time):
    cooldown_monitor[function] = cooldown_monitor.get(function, {'in_cooldown': False,
                                                                 'cooldown_message_sent': False,
                                                                 'recent_calls': ExpiringDict(max_age_seconds=within_timelimit)})

    if cooldown_monitor[function]['in_cooldown'] and len(cooldown_monitor[function]['recent_calls']) >= number_of_calls:
        cooldown_monitor[function]['in_cooldown'] = True
    else:
        cooldown_monitor[function]['recent_calls'][uuid.uuid1()] = True
        if len(cooldown_monitor[function]['recent_calls']) >= number_of_calls:
            cooldown_monitor[function]['in_cooldown'] = True
            cooldown_monitor[function]['cooldown_message_sent'] = False
            timer = Timer(cooldown_for_time, out_of_cooldown_callback, [function])
            timer.start()
    return cooldown_monitor[function]['in_cooldown']
