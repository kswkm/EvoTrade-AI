import logging.config
from typing import Any


LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    },
}


def configure_logging(log_level: str = "INFO") -> None:
    config = dict(LOGGING_CONFIG)
    config["loggers"] = {
        "": {
            "handlers": ["console"],
            "level": log_level.upper(),
            "propagate": False,
        }
    }
    logging.config.dictConfig(config)
