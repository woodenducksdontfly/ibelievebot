import messagehandler
from datetime import datetime
from data_handlers import static

# Quotes from all factions of life
quotes = static.file_handler.get_file_data('wisdom.json')


@messagehandler.register("twitch", "!wisdom")
@messagehandler.register("discord", "!wisdom")
def wisdom(bot, sent_by, msg_text, channel=None):
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(quotes)
    bot.write_to_chat("Quote #{}: {}".format(index+1, quotes[index]), channel)
