import logging


def get_simple_logger(filename: str) -> logging.Logger:
    logger = logging.getLogger("simple_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=filename)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger

logger = get_simple_logger("app/logger.log")