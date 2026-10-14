from .validator import AuthValidator
from .db import RegistrationDB
from .interfaces import AbstractUserInterface, AbstractExternalService

SUCCESS_MESSAGE = "Регистрация прошла успешно"
DEFAULT_ERROR_MESSAGE = "Ошибка регистрации"


class Controller:
    def __init__(
        self,
        validator: AuthValidator,
        db: RegistrationDB,
        ui: AbstractUserInterface,
        external: AbstractExternalService,
    ) -> None:
        self.validator = validator
        self.db = db
        self.ui = ui
        self.external = external

    def run(self) -> tuple[bool, str]:
        login, password, confirm = self.ui.get_credentials()

        existing = self.db.get(login, password, confirm)
        if existing is not None:
            ok = existing["auth_result"]
            message = self._result_message(ok, existing["error_message"])
        else:
            ok, error = self.validator.validate(login, password, confirm)
            message = self._result_message(ok, error)
            self.db.add(login, password, confirm, ok, "" if ok else message)

        self.external.send(f"success: {ok}, message: {message}")
        return ok, message

    @staticmethod
    def _result_message(ok: bool, error: str) -> str:
        if ok:
            return SUCCESS_MESSAGE
        return error or DEFAULT_ERROR_MESSAGE
