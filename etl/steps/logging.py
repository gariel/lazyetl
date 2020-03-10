import enum
import logging

from etl.common import StepController


class LogLevel(enum.IntEnum):
    Error = logging.ERROR,
    Warning = logging.WARNING,
    Info = logging.INFO,
    Debug = logging.DEBUG


class Logging(StepController):
    def log(self, level: LogLevel, message: str):
        # self.ctx.logger.log(level.value, message)
        print(level, message)
