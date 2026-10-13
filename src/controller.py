from .validator import AuthValidator
from .db import RegistrationDB
from .interfaces import AbstractUserInterface, AbstractExternalService


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
            success = bool(existing["auth_result"])
            message = existing["error_message"] or ""
            if success:
                result_str = (
                    f"success: True, message: Регистрация прошла успешно"
                )
            else:
                msg = message or "Ошибка регистрации"
                result_str = f"success: False, message: {msg}"
            self.external.send(result_str)
            return success, message

        ok, msg = self.validator.validate(login, password, confirm)
        if ok:
            message_out = "Регистрация прошла успешно"
        else:
            message_out = msg or "Ошибка регистрации"

        self.db.add(login, password, confirm, ok, message_out if not ok else "")

        if ok:
            result_str = f"success: True, message: {message_out}"
        else:
            result_str = f"success: False, message: {message_out}"
        self.external.send(result_str)
        return ok, message_out
