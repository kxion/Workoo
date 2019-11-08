import os
import logging
from logging.handlers import RotatingFileHandler


def init_log():

    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(level=logging.INFO)
    if not logger.handlers:
        try:
            handler = RotatingFileHandler(
                "./log/run_info.log",
                maxBytes=10 * 1024 * 1024,
                backupCount=100)
            # handler = loggingFileHandler("./log/run_info.log")
        except FileNotFoundError as exc:
            os.makedirs("./log/")
            return init_log()

        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)

        logger.addHandler(handler)
        logger.addHandler(console)
        

    return logger