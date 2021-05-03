import logging


def setup_logger(name: str, log_file: str, log_format: str = "%(levelname)s:%(name)s:%(asctime)s:%(message)s",
                 date_format: str = "%D:%H.%M.%S", log_level: int = logging.INFO) -> logging.Logger:
    """
    Creates new logger from the logging module with ease and returns it

    To use a custom log format, use the keyword argument log_format with your custom format, e.g.

    log_controller.setup_logger(__name__, "log_file.log", log_format="%(levelname)s:%(message)s")

    To use a custom date/time format, use the keyword argument date_format with your custom format, e.g.

    log_controller.setup_logger(__name__, "log_file.log", date_format="%H:%M:%S")

    To use a different log level, use the keyword argument log_level with your desired level, e.g.

    log_controller.setup_logger(__name__, "log_file.log", log_level=logging.ERROR)

    Args:
        name (str): The name of the module that the logger will log from.
        log_file (strl): The filename of the log file we're logging to.
        log_format (str, optional): The log format defaults to "%(levelname)s:%(name)s:%(asctime)s:%(message)s",
            but if a different format is given, the new format will be used instead.
        date_format (str, optional): The date format defaults to "%D:%H.%M.%S",
            but if a different format is given, the new format will be used instead.
        log_level (int, optional): The log level defaults to logging.INFO (20),
            but if a different level is given, the logger will be setup with the new level.

    Returns:
        logging.Logger: the logger that was just constructed.
    """

    # creating the file handler
    formatter = logging.Formatter(log_format, datefmt=date_format)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter, )

    # creating the main logger
    logger = logging.getLogger(name)  # defines the actual logger
    logger.setLevel(log_level)  # sets logger level
    logger.addHandler(handler)  # adds handler to logger

    return logger


def empty_log(logger: logging.Logger):
    """
    Empties the file attached to a log handler

    Args:
        logger (logging.Logger): The logger whose log file you wish to empty
    """

    # gets handler and pulls log filename from it
    file_handler = logger.handlers[0]
    handler_file = file_handler.baseFilename
    # opens the file for writing (not appending) which basically empties it and then just closes it
    open(handler_file, 'w').close()
