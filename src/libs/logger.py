"""
Contains all logging-related code for the project.
"""
import logging
import os


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg: str, datefmt: str = None, use_color: bool = True):
        if datefmt is not None:
            super().__init__(msg, datefmt)
        else:
            super().__init__(msg)

        self.use_color = use_color
        RESET_SEQ = "\033[0m"
        COLOR_SEQ = "\033[38;5;%dm"
        BOLD_SEQ = "\033[1;38;5;%dm"
        # colors
        RED = 196
        GREEN = 190
        YELLOW = 220
        BLUE = 21
        MAGENTA = 201
        CYAN = 33
        WHITE = 231

        # formats
        self.FORMATS = {
            logging.DEBUG: (COLOR_SEQ % MAGENTA) + msg + RESET_SEQ,
            logging.INFO: (COLOR_SEQ % WHITE) + msg + RESET_SEQ,
            logging.WARNING: (COLOR_SEQ % YELLOW) + msg + RESET_SEQ,
            logging.ERROR: (COLOR_SEQ % RED) + msg + RESET_SEQ,
            logging.CRITICAL: (BOLD_SEQ % RED) + msg + RESET_SEQ
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.datefmt)
        d = formatter.format(record)
        # %(levelname)s (%(asctime)s) - %(name)s: %(message)s (Line: %(lineno)d [%(filename)s])
        # 'CRITICAL' '08/27 22:03:34' - 'main': 'We are going critical' (Line: '103' ['test.py'])
        return d


def setupLogging(LoggerName: str, level: int = 10, FileHandler: logging.FileHandler = None,
                 ConsoleHandler: logging.StreamHandler = None) -> logging.Logger:
    """
    A simple function to set up a logger based on the name given
    :param LoggerName: A string which has the name of the logger to give to logging.getLogger()
    :param level: The lowest level to output from the logger (optional defaults to logging.DEBUG)
    :param FileHandler: If you want a custom FileHandler for your logger (optional defaults to the one defined in function)
    :param ConsoleHandler: If you want a custom StreamHandler for your logger (optional defaults to the one defined in the function)
    :return: logging.Logger
    """
    logger: logging.Logger = logging.getLogger(LoggerName)
    logFormatter = logging.Formatter(
        "%(levelname)s (%(asctime)s) - %(name)s: %(message)s (Line: %(lineno)d [%(filename)s])",
        "%m/%d %H:%M:%S"
    )
    logFormatterColored = ColoredFormatter(
        "%(levelname)s (%(asctime)s) - %(name)s: %(message)s (Line: %(lineno)d [%(filename)s])",
        "%m/%d %H:%M:%S",
        use_color=True
    )

    if FileHandler is None:
        if not os.path.exists("./logs/"):
            os.mkdir("./logs")

        if not os.path.exists("./logs/console.log"):
            with open("./logs/console.log", "w"):
                pass

        fileHandler = logging.FileHandler(
            "{0}/{1}.log".format("./logs", "console")
        )
    else:
        fileHandler = FileHandler
    fileHandler.setFormatter(logFormatter)

    if ConsoleHandler is None:
        consoleHandler = logging.StreamHandler()
    else:
        consoleHandler = ConsoleHandler
    consoleHandler.setFormatter(logFormatterColored)

    logger.level = level
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


class LoggingBase:
    """
    Base class to automatically declare logging configuration
    """
    def __init__(self, level: int = logging.INFO):
        self.logger = setupLogging(self.__class__.__name__, level)
