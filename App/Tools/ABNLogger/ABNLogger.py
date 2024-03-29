import datetime
#import logging
import os
import sys
print('Our ABN Logger 2/16/2023')

from abc import abstractmethod
from PytomatedLiquidHandling.Tools.AbstractClasses import ObjectABC


class ABNLogger(ObjectABC):
    def __init__(
        self,
        ABNLoggerDict: dict
    ):

    @abstractmethod
    def GetBlockAttributesForLogging(self, Block):
        BlockName = Block.Name
        BlockExcelInstance = Block.ExcelInstance
        BlockRow = Block.Row
        BlockCol = Block.Col

        if [BlockName, BlockExcelInstance, BlockRow, BlockCol] not in self.ABNLoggerDict.keys():
            self.ABNLoggerDict[[BlockName, BlockExcelInstance, BlockRow, BlockCol]] = {}
        else:
            print('ERROR: The following block informatoin already exists in the ABN logging dictionary, ABNLoggerDict')
            print([BlockName, BlockExcelInstance, BlockRow, BlockCol])

        return self.ABNLoggerDict

'''
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "[%(asctime)s] %(levelname)s\n%(message)s\n(%(threadName)s).%(module)s.%(funcName)s:%(lineno)d) <%(pathname)s>"

LOG = logging.getLogger(__name__)

BASE_DIRECTORY = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    ),
    "Logging",
)
LOG_DIRECTORY = os.path.join(BASE_DIRECTORY, "LogFiles")
TIME = str(datetime.datetime.now().strftime("%d%b%Y-%H%M%S"))
BASE_LOGFILE_NAME = "Log.ansi"
LOG_FILE_FULL_PATH = os.path.join(LOG_DIRECTORY, TIME + BASE_LOGFILE_NAME)

os.makedirs(LOG_DIRECTORY, exist_ok=True)


class STDERRLogger(object):
    def __init__(self):
        self.Message = ""

    def write(self, message):
        self.Message += message

    def flush(self):
        if self.Message != "":
            LOG.critical(self.Message)
        self.Message = ""


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    debug = "\x1b[38;5;255m"
    info = "\x1b[38;5;39m"
    warning = "\x1b[38;5;226m"
    error = "\x1b[38;5;208m"
    critical = "\x1b[31;5;196m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.debug + self.fmt + self.reset,
            logging.INFO: self.info + self.fmt + self.reset,
            logging.WARNING: self.warning + self.fmt + self.reset,
            logging.ERROR: self.error + self.fmt + self.reset,
            logging.CRITICAL: self.critical + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


LOG.setLevel(LOG_LEVEL)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(LOG_LEVEL)
stdout_handler.setFormatter(CustomFormatter(LOG_FORMAT))

file_handler = logging.FileHandler(LOG_FILE_FULL_PATH)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(CustomFormatter(LOG_FORMAT))

LOG.addHandler(stdout_handler)
LOG.addHandler(file_handler)

sys.stderr = STDERRLogger()

LOG.debug("Debug Message")
LOG.info("Info Message")
LOG.warning("Warning Message")
LOG.error("Error Message")
LOG.critical("Critical Message")
'''