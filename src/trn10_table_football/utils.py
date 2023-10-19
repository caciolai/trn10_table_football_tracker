import logging

from trn10_table_football.constants import LOG_FILE

def setup_logger(root=None):
    logger = logging.getLogger(root)
    logger.setLevel(logging.INFO)

    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    consolehandler = logging.StreamHandler()
    consolehandler.setLevel(logging.INFO)
    consolehandler.setFormatter(format)
    logger.addHandler(consolehandler)

    filehandler = logging.FileHandler(LOG_FILE)
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(format)
    logger.addHandler(filehandler)

    # send logs to root logger, which will decide where all logs are stored
    logger.propagate = False
    return logger