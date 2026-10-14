import unittest
from unittest.mock import patch

from src.interfaces import AbstractUserInterface
from src.ui_console import ConsoleUserInterface


class TestConsoleUserInterface(unittest.TestCase):
    def test_implements_interface(self):
        self.assertIsInstance(ConsoleUserInterface(), AbstractUserInterface)

    def test_get_credentials_asks_three_values(self):
        ui = ConsoleUserInterface()
        with patch(
            "builtins.input",
            side_effect=["alice123", "Пароль123!", "Пароль123!"],
        ) as mock_input:
            credentials = ui.get_credentials()

        self.assertEqual(credentials, ("alice123", "Пароль123!", "Пароль123!"))
        self.assertEqual(mock_input.call_count, 3)
        self.assertIn("логин", mock_input.call_args_list[0].args[0])
        self.assertIn("Повторите пароль", mock_input.call_args_list[2].args[0])


if __name__ == "__main__":
    unittest.main()
