import logging


class Logging:
    def __init__(self):
        logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def debug(message):
        logging.debug(message)

    @staticmethod
    def critical(message):
        logging.critical(message)

    @staticmethod
    def exception(message):
        logging.exception(message)
