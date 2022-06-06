import logging


# TODO need a logging server since writing to a file is not multi thread safe
# https://docs.python.org/3/howto/logging-cookbook.html

# TODO roll log daily & every 100 MB

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    log_format_str = '{"namespace": "%(name)s", "timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"},'
    log_formatter = logging.Formatter(log_format_str)
    file_handler = logging.FileHandler('stream_logs/ibelievebot.log')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    return logger
