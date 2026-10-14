import logging

from .logger import setup_logging
from .validator import AuthValidator
from .db import RegistrationDB
from .ui_console import ConsoleUserInterface
from .external import DummyExternalService
from .controller import Controller


def main() -> None:
    setup_logging()

    validator = AuthValidator()
    db = RegistrationDB()
    ui = ConsoleUserInterface()
    external = DummyExternalService()
    controller = Controller(validator, db, ui, external)

    while True:
        try:
            success, message = controller.run()
        except EOFError:
            print("\nВвод завершён. Программа остановлена.")
            return
        except TypeError:
            logging.exception("Ошибка: Некорректные данные")
            print(
                "Ошибка: Некорректные данные. "
                "Пожалуйста, введите строковые значения."
            )
            continue
        except Exception:
            logging.exception(
                "Непредвиденная ошибка при регистрации"
            )
            print(
                "Произошла непредвиденная ошибка. "
                "Проверьте логи."
            )
            continue

        if not success:
            print(f"Ошибка: {message}")
            continue

        print("Регистрация прошла успешно")
        break


if __name__ == "__main__":
    main()
