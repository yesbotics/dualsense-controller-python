from __future__ import annotations

import enum
import logging
from typing import Any, Final, Iterable

NAME_LOGGER: Final[str] = "DSC_LOGGER"


class LogLevel(enum.IntEnum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    VERBOSE = 15
    DEBUG = logging.DEBUG
    TRACE = 5
    NOTSET = logging.NOTSET


class Log:
    __DEFAULT_FORMATTER: Final[logging.Formatter] = logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s')

    __instance: Log = None

    def __init__(self):
        logging.addLevelName(LogLevel.TRACE, LogLevel.TRACE.name)
        logging.addLevelName(LogLevel.VERBOSE, LogLevel.VERBOSE.name)

        self.__logger: logging.Logger = logging.getLogger(NAME_LOGGER)
        self.__logger.setLevel(LogLevel.INFO)

        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.formatter = self.__DEFAULT_FORMATTER
        self.__logger.addHandler(stream_handler)

    @classmethod
    def __get_instance(cls):
        if cls.__instance is None:
            cls.__instance = Log()
        return cls.__instance

    @classmethod
    def set_level(cls, level: LogLevel):
        cls.__get_instance().__logger.setLevel(level)

    @classmethod
    def critical(cls, msg, *args: Any):
        cls.__get_instance().__logger.critical(cls.__args_to_str(msg, *args))

    @classmethod
    def fatal(cls, msg, *args: Any):
        cls.__get_instance().__logger.fatal(cls.__args_to_str(msg, *args))

    @classmethod
    def error(cls, msg, *args: Any):
        cls.__get_instance().__logger.error(cls.__args_to_str(msg, *args))

    @classmethod
    def exception(cls, exception: BaseException, *args: Any):
        cls.__get_instance().__logger.exception(exception)

    @classmethod
    def warning(cls, msg, *args: Any):
        cls.__get_instance().__logger.warning(cls.__args_to_str(msg, *args))

    @classmethod
    def info(cls, msg, *args: Any):
        cls.__get_instance().__logger.info(cls.__args_to_str(msg, *args))

    @classmethod
    def verbose(cls, msg, *args: Any):
        cls.__get_instance().__logger.log(LogLevel.VERBOSE, cls.__args_to_str(msg, *args))

    @classmethod
    def debug(cls, msg, *args: Any):
        cls.__get_instance().__logger.debug(cls.__args_to_str(msg, *args))

    @classmethod
    def trace(cls, msg, *args: Any):
        cls.__get_instance().__logger.log(LogLevel.TRACE, cls.__args_to_str(msg, *args))

    @classmethod
    def __args_to_str(cls, msg, *args: Any) -> str:
        args_as_str: Iterable[str] = map(lambda arg: str(arg), args)
        msg = str(msg)
        msg = f'{msg}, ' if len(args) else msg
        return f'{msg}{", ".join(args_as_str)}'
