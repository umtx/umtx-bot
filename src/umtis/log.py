import logging
import os

from logging import config as logging_config


# logging.basicConfig(level=100, filename='debug.log', format='[%(asctime)s] - %(levelname)s: %(message)s')


def setup_logging(name='ticketbot'):
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def set_to_file(output):
    logging.basicConfig(level=logging.DEBUG, filename=output,
                        format='[%(asctime)s] - %(levelname)s: %(message)s')


def get_logger(file):
    LOG_PATH = "{home}/ticketbot/log/{file}".format(
        home=os.getenv("HOME"), file=file)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        'formatters': {
            'info': {
                'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
            },
            'error': {
                'format': '%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s'
            },
            'default': {
                'format': '%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s'
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": LOG_PATH,
                # 16 MB
                "maxBytes": 16 * 1024 * 1024,
                "mode": "a",
                "backupCount": 5,
                "level": "INFO"
            }
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    }

    logging_config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger()
    return logger
