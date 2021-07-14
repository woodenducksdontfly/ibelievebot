import messagehandler
from datetime import datetime
from file_handler import static

# Quotes from yogi tea tags
quotes = static.file_handler.get_file_data('yogi.json')


@messagehandler.register("twitch", "!yogi")
@messagehandler.register("discord", "!yogi")
def yogi(bot, sent_by, msg_text, channel=None):
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(quotes)
    response = "Quote #{}: {}".format(index+1, quotes[index])
    bot.write_to_chat(response, channel)
