import logging
import logging.config

import json

LOG_CONFIG_FILE = "logs/logging_config.json"

with open(LOG_CONFIG_FILE, 'r') as conf:
    config_dict = json.load(conf)
logging.config.dictConfig(config_dict)
logger = logging.getLogger("TrainSearch")
