from .interfaces import AbstractUserInterface


class ConsoleUserInterface(AbstractUserInterface):
    def get_credentials(self) -> tuple[str, str, str]:
        login = input("Введите логин (телефон или email): ")
        password = input("Введите пароль: ")
        password_confirm = input("Повторите пароль: ")
        return login, password, password_confirm
