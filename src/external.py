import logging

from .interfaces import AbstractExternalService


class DummyExternalService(AbstractExternalService):
    def send(self, result: str) -> None:
        logging.info(f"Отправка результата стороннему сервису: {result}")
