import logging
import logging.config
import os

from logging_config import LOGGING_CONFIG

logfolder = os.path.dirname(os.path.abspath(__file__))

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging

