import sys
import logging.config
import coloredlogs


logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] #%(levelname)-8s - %(message)s"
        },
        "outer_style": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": sys.stdout
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "default",
            "stream": sys.stderr
        },
        "outer_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "outer_style",
            "stream": sys.stdout
        }
    },
    "loggers": {
        "outer": {
            "handlers": ["outer_handler"],
            "level": "INFO",
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "formatter": "default",
        "handlers": ["stdout"]
    }
}


def load_logger_config():
    # Применяем конфигурацию логирования
    logging_config["handlers"]["stdout"]["formatter"] = "default"
    logging.config.dictConfig(logging_config)

    # Устанавливаем цветное форматирование для корневого логгера
    coloredlogs.install(
        level=logging_config["root"]["level"],
        fmt=
        logging_config['formatters'][logging_config["handlers"]["stdout"]["formatter"]][
            'format'],
        logger=logging.getLogger()  # Применяем ко всему
    )

    # Устанавливаем цветное форматирование для логгера yt-dlp
    outer_logger = logging.getLogger('outer')
    coloredlogs.install(
        level=outer_logger.level,
        fmt=logging_config['formatters']['outer_style']['format'],
        logger=outer_logger
    )