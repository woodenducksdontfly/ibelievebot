import inspect

import messagehandler
import cooldown


@messagehandler.register("twitch", "!look")
def look(bot, sent_by, msg_text, channel=None):
    if messagehandler.is_user_elevated(bot, channel, sent_by):
        function_name = inspect.stack()[1][3]
        in_cooldown = cooldown.cooldown(function=function_name,
                                        number_of_calls=5,
                                        within_timelimit=60,
                                        cooldown_for_time=500)
        if in_cooldown and not cooldown.is_cooldown_message_sent(function_name):
            bot.write_to_chat("Look is in cooldown, please don't spam chat", channel)
            cooldown.set_cooldown_message_sent(function_name)
            return
        try:
            extra_command = msg_text.split(' ', 1)[1]
            with open('data/look.txt', 'a', newline='\n') as f:
                f.write(extra_command + '\n')
            bot.write_to_chat('Thanks', channel)
        except IndexError:
            pass
        except Exception as e:
            print(e)

#
# @messagehandler.register("twitch", "!cookie")
# def cookie(bot, sent_by, msg_text, channel=None):
#     try:
#         extra_command = msg_text.split(' ', 1)[1]
#         with open('data/cookies.txt', 'a', newline='\n') as f:
#             f.write("Sent By {}: {}\n".format(sent_by, extra_command))
#         bot.write_to_chat('Cookie submitted, Thanks!', channel)
#     except IndexError:
#         bot.write_to_chat("Baking stream June 6th or 7th, type \"!cookie cookie_name\" to submit your favorite cookie so I can investigate the best rolled cookies before then.  I'll only make one.  No drop cookies this round.", channel)
#     except Exception as e:
#         print(e)
