import unittest
from unittest.mock import Mock

from src.validator import AuthValidator
from src.db import RegistrationDB
from src.controller import Controller


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.validator = AuthValidator()
        self.db = RegistrationDB(":memory:")
        self.ui = Mock()
        self.external = Mock()

    def tearDown(self):
        self.db.close()

    def test_integration_no_record_success(self):
        self.ui.get_credentials.return_value = ("alice123", "Пароль123!", "Пароль123!")

        controller = Controller(self.validator, self.db, self.ui, self.external)
        success, message = controller.run()

        self.assertTrue(success)
        self.assertIn("успешно", message)

        row = self.db.get("alice123", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(row)
        self.assertTrue(row["auth_result"])

        self.external.send.assert_called_once()
        sent_arg = self.external.send.call_args[0][0]
        self.assertIn("success: True", sent_arg)

    def test_integration_record_exists_from_db(self):
        self.db.add("bob456", "Пароль123!", "Пароль123!", True, "")

        validator_mock = Mock(wraps=self.validator)
        self.ui.get_credentials.return_value = ("bob456", "Пароль123!", "Пароль123!")

        controller = Controller(validator_mock, self.db, self.ui, self.external)
        success, message = controller.run()

        self.assertTrue(success)
        self.assertEqual(message, "")

        validator_mock.validate.assert_not_called()

        self.external.send.assert_called_once()
        sent_arg = self.external.send.call_args[0][0]
        self.assertIn("success: True", sent_arg)

    def test_integration_validation_error_saved_and_sent(self):
        self.ui.get_credentials.return_value = ("admin", "Пароль123!", "Пароль123!")

        controller = Controller(self.validator, self.db, self.ui, self.external)
        success, message = controller.run()

        self.assertFalse(success)
        self.assertIn("черном списке", message)

        row = self.db.get("admin", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(row)
        self.assertFalse(row["auth_result"])
        self.assertIn("черном списке", row["error_message"])

        self.external.send.assert_called_once()
        sent_arg = self.external.send.call_args[0][0]
        self.assertIn("success: False", sent_arg)
        self.assertIn("черном списке", sent_arg)

    def test_integration_password_mismatch(self):
        self.ui.get_credentials.return_value = ("testuser", "Пароль123!", "Пароль123")

        controller = Controller(self.validator, self.db, self.ui, self.external)
        success, message = controller.run()

        self.assertFalse(success)
        self.assertIn("не совпадают", message)

        row = self.db.get("testuser", "Пароль123!", "Пароль123")
        self.assertIsNotNone(row)
        self.assertFalse(row["auth_result"])

        self.external.send.assert_called_once()

    def test_integration_cached_error_on_second_call(self):
        creds = ("baduser", "Пароль", "Пароль")
        self.ui.get_credentials.return_value = creds

        validator_mock = Mock(wraps=self.validator)
        controller = Controller(validator_mock, self.db, self.ui, self.external)
        success1, msg1 = controller.run()
        self.assertFalse(success1)

        self.ui.get_credentials.return_value = creds
        success2, msg2 = controller.run()
        self.assertFalse(success2)
        self.assertEqual(msg1, msg2)

        self.assertEqual(validator_mock.validate.call_count, 1)

        self.assertGreaterEqual(self.external.send.call_count, 2)


if __name__ == "__main__":
    unittest.main()
