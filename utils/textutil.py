
import html
from better_profanity import profanity


# profanity.load_censor_words(whitelist_words=['happy', 'merry'])
profanity.load_censor_words()


def sanitize_text(msg):
    """
    Get html safe text only
    Trim
    Parse out bad words
    # replace emote text with emote images
    # create html object
    # add html object to label and add to chat
    :param msg:
    :return:
    """
    clean_message = profanity.censor(html.escape(msg).strip())
    return clean_message
