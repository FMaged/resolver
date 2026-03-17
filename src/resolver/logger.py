import logging

class JSONFormatter(logging.Formatter):
    pass

def get_logger():
    logging.config.dictConfig(config=logging_config)
    return logging.getLogger("Xdig")    