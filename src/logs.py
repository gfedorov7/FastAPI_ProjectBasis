import logging
import logging.config


def setup_logging():
    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)