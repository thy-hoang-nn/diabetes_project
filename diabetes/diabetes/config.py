import logging
from rich.logging import RichHandler
import os
import sys
from logging import config
from pathlib import Path


# from dotenv import load_dotenv


# load_dotenv()


# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()

# config.py
LOGS_DIR = Path(BASE_DIR, "logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
# Package dirs
PACKAGE_DIR = Path(BASE_DIR, "diabetes")

EXAMPLE_DIR = Path(BASE_DIR, "example")

MODEL_DIR = Path(PACKAGE_DIR, "models", "gscv-0.843.sav")


DATA_DIR = Path(PACKAGE_DIR, "data", "diabetes.csv")


dir = os.listdir()

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": (
                "%(levelname)s %(asctime)s [%(name)s:%(filename)s:            "
                "    %(funcName)s:%(lineno)d]\n%(message)s\n"
            )
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "root": {
        "handlers": ["console", "info", "error"],
        "level": logging.INFO,
        "propagate": True,
    },
}

# config/config.py
config.dictConfig(logging_config)
logger = logging.getLogger()
logger.handlers[0] = RichHandler(markup=True)  # pretty formatting
logger.level = 20
