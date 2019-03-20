import logging


def get_configured_logger(loggername, filename):
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s %(name)10s:%(funcName)-30s: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
