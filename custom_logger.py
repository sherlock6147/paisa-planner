import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime, timedelta, timezone

class ISTFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        ist = timezone(timedelta(hours=5, minutes=30))  # Indian Standard Time (IST) offset
        dt = dt.replace(tzinfo=timezone.utc).astimezone(ist)
        return dt.timetuple()

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            s = datetime.strftime(self.default_time_format, dt)
        return s

# Ensure the 'logs' directory exists
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
formatter = ISTFormatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')

def get_logger(name)->Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(os.path.join(log_directory, 'paisa_planner.log'), maxBytes=1000*1000, backupCount=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger