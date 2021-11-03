import messagehandler
from datetime import datetime
from data_handlers import static

# Quotes from other tea tags
quotes = static.file_handler.get_file_data('tea.json')


@messagehandler.register("twitch", "!tea")
@messagehandler.register("discord", "!tea")
def tea(bot, sent_by, msg_text, channel=None):
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(quotes)
    bot.write_to_chat("Quote #{}: {}".format(index+1, quotes[index]), channel)
