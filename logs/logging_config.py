import os
from definitions import ROOT_DIR

MAIL_ADDRESS = "riccardo.maganza@gmail.com"
OAUTH_PATH = os.path.join(ROOT_DIR, "secret", "oauth2.json")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        "mail_handler": {
            "class": "logs.GMailHandler.GMailHandler",
            "level": "CRITICAL",
            "oauth_path": OAUTH_PATH,
            "fromaddr": MAIL_ADDRESS,
            "subject": "*CRITICAL* TrainSearch Error"
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": os.path.join(ROOT_DIR, 'logs', 'trainlog.log'),
            "encoding": "utf8"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["file_handler", "mail_handler"]
    }
}