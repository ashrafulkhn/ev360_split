"""
Common utility functions for PECC system.
Modular and reusable helpers for logging, validation, etc.
"""

import logging
from datetime import datetime
import websockets

# Custom logger with timestamp to milliseconds
class MilliSecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = datetime.fromtimestamp(record.created)
        return t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

formatter = MilliSecondFormatter('INFO:pecc:%(asctime)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('pecc')
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)

# Add more utility functions as needed
class Versions:
    WEBSOCKET_OLD = False  # Class variable

    @classmethod
    def detect_websocket_version(cls):
        """Detects installed websocket version and sets WEBSOCKET_OLD automatically"""
        try:
            version_tuple = tuple(map(int, websockets.__version__.split(".")))
            cls.WEBSOCKET_OLD = version_tuple <= (10, 1)
        except Exception:
            cls.WEBSOCKET_OLD = False

    @classmethod
    def check_if_websocket_old(cls):
        return cls.WEBSOCKET_OLD

# Auto-detect on import
Versions.detect_websocket_version()