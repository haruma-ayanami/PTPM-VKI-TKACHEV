from abc import ABC, abstractmethod


class AbstractUserInterface(ABC):
    @abstractmethod
    def get_credentials(self) -> tuple[str, str, str]:
        """Возвращает (login, password, confirm_password)"""
        pass


class AbstractExternalService(ABC):
    @abstractmethod
    def send(self, result: str) -> None:
        """Имитация отправки строки-результата сторонней зависимости"""
        pass
