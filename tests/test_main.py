import contextlib
import io
import unittest
from unittest.mock import Mock, patch

from src.main import main


class _StopLoop(BaseException):
    """Не перехватывается `except Exception` в main(): если цикл не остановится, тест упадёт, а не зависнет."""


class TestMain(unittest.TestCase):
    def setUp(self):
        setup_patch = patch("src.main.setup_logging")
        logging_patch = patch("src.main.logging")
        self.setup_logging = setup_patch.start()
        self.logging = logging_patch.start()
        self.addCleanup(setup_patch.stop)
        self.addCleanup(logging_patch.stop)

    def run_main(self, inputs=None):
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(out):
            main()
        return out.getvalue()

    def test_successful_registration_stops_loop(self):
        output = self.run_main(["alice123", "Пароль123!", "Пароль123!"])

        self.assertIn("Регистрация прошла успешно", output)
        self.setup_logging.assert_called_once()

    def test_invalid_input_asks_again(self):
        output = self.run_main([
            "alice123", "Пароль123!", "Пароль123",
            "alice123", "Пароль123!", "Пароль123!",
        ])

        self.assertIn("Ошибка: Пароли не совпадают", output)
        self.assertIn("Регистрация прошла успешно", output)

    def test_eof_stops_program(self):
        output = self.run_main([EOFError(), _StopLoop()])

        self.assertIn("Ввод завершён", output)

    def test_type_error_is_reported_and_retried(self):
        controller = Mock()
        controller.run.side_effect = [TypeError(), (True, "")]
        with patch("src.main.Controller", return_value=controller):
            output = self.run_main()

        self.assertIn("Некорректные данные", output)
        self.logging.exception.assert_called_once()

    def test_unexpected_error_is_reported_and_retried(self):
        controller = Mock()
        controller.run.side_effect = [RuntimeError("boom"), (True, "")]
        with patch("src.main.Controller", return_value=controller):
            output = self.run_main()

        self.assertIn("непредвиденная ошибка", output)
        self.logging.exception.assert_called_once()


if __name__ == "__main__":
    unittest.main()
