import unittest

from src.db import RegistrationDB


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = RegistrationDB(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get(self):
        self.db.add("alice123", "Пароль123!", "Пароль123!", True, "")
        row = self.db.get("alice123", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(row)
        self.assertEqual(row["login"], "alice123")
        self.assertTrue(row["auth_result"])
        self.assertEqual(row["error_message"], "")

    def test_get_not_found(self):
        row = self.db.get("nope", "Пароль123!", "Пароль123!")
        self.assertIsNone(row)

    def test_add_with_error(self):
        self.db.add("alice123", "Пароль", "Пароль", False, "Пароли не совпадают")
        row = self.db.get("alice123", "Пароль", "Пароль")
        self.assertIsNotNone(row)
        self.assertFalse(row["auth_result"])
        self.assertIn("не совпадают", row["error_message"])

    def test_delete_existing(self):
        self.db.add("bob456", "Пароль123!", "Пароль123!", True, "")
        deleted = self.db.delete("bob456", "Пароль123!", "Пароль123!")
        self.assertTrue(deleted)
        row = self.db.get("bob456", "Пароль123!", "Пароль123!")
        self.assertIsNone(row)

    def test_delete_not_existing(self):
        deleted = self.db.delete("missing", "Пароль123!", "Пароль123!")
        self.assertFalse(deleted)

    def test_key_uniqueness(self):
        self.db.add("user1", "Пароль123!", "Пароль123!", True, "")
        self.db.add("user1", "Пароль123!", "Пароль123!", False, "другая ошибка")
        row = self.db.get("user1", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(row)
        self.assertTrue(row["auth_result"])
        self.assertEqual(row["error_message"], "")


if __name__ == "__main__":
    unittest.main()
