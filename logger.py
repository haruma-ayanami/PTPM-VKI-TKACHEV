import logging
import os
import sys

LOG_FORMAT = "%(asctime)s | [%(levelname)-7s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")
