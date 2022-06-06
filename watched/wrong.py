import inspect

import messagehandler
import cooldown
from data_handlers import stream


@messagehandler.register("twitch", "!wrongchat")
def wrongchat(bot, sent_by, msg_text, channel=None):
    function_name = inspect.stack()[1][3]
    in_cooldown = cooldown.cooldown(function=function_name,
                                    number_of_calls=2,
                                    within_timelimit=60,
                                    cooldown_for_time=100)
    if in_cooldown:
        if not cooldown.is_cooldown_message_sent(function_name):
            bot.write_to_chat("wrongchat is in cooldown, please don't spam chat", channel)
            cooldown.set_cooldown_message_sent(function_name)
        return
    stream.stream_data_handler.increment_wrongs()
    bot.write_to_chat("Chat has been wrong {} times!".format(stream.stream_data_handler.get_wrongs()), channel)
