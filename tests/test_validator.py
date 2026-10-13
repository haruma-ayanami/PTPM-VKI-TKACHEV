import unittest

from src.validator import AuthValidator, mask_password


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = AuthValidator()

    def test_mask_password_deterministic(self):
        h1 = mask_password("Passw0rd!")
        h2 = mask_password("Passw0rd!")
        self.assertEqual(h1, h2)
        self.assertTrue(len(h1) == 16)

    def test_login_valid_email(self):
        ok, msg = self.validator.validate("user@example.com", "Пароль123!", "Пароль123!")
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_login_valid_phone(self):
        ok, msg = self.validator.validate("+7-900-123-4567", "Пароль123!", "Пароль123!")
        self.assertTrue(ok)

    def test_login_valid_simple(self):
        ok, msg = self.validator.validate("alice123", "Пароль123!", "Пароль123!")
        self.assertTrue(ok)

    def test_login_empty(self):
        ok, msg = self.validator.validate("", "Пароль123!", "Пароль123!")
        self.assertFalse(ok)
        self.assertIn("пустым", msg)

    def test_login_blacklist(self):
        ok, msg = self.validator.validate("admin", "Пароль123!", "Пароль123!")
        self.assertFalse(ok)
        self.assertIn("черном списке", msg)

    def test_login_too_short(self):
        ok, msg = self.validator.validate("abc", "Пароль123!", "Пароль123!")
        self.assertFalse(ok)
        self.assertIn("минимум 5", msg)

    def test_login_invalid_chars(self):
        ok, msg = self.validator.validate("юзер123", "Пароль123!", "Пароль123!")
        self.assertFalse(ok)
        self.assertIn("только латиницу", msg)

    def test_password_mismatch(self):
        ok, msg = self.validator.validate("testuser", "Пароль123!", "Пароль123")
        self.assertFalse(ok)
        self.assertIn("не совпадают", msg)

    def test_password_too_short(self):
        ok, msg = self.validator.validate("testuser", "Пар12!", "Пар12!")
        self.assertFalse(ok)
        self.assertIn("минимум 7", msg)

    def test_password_no_lower(self):
        ok, msg = self.validator.validate("testuser", "ПАРОЛЬ123!", "ПАРОЛЬ123!")
        self.assertFalse(ok)
        self.assertIn("нижнем регистре", msg)

    def test_password_no_upper(self):
        ok, msg = self.validator.validate("testuser", "пароль123!", "пароль123!")
        self.assertFalse(ok)
        self.assertIn("верхнем регистре", msg)

    def test_password_no_digit(self):
        ok, msg = self.validator.validate("testuser", "Пароль!!", "Пароль!!")
        self.assertFalse(ok)
        self.assertIn("цифры", msg)

    def test_password_no_special(self):
        ok, msg = self.validator.validate("testuser", "Пароль123", "Пароль123")
        self.assertFalse(ok)
        self.assertIn("спецсимвола", msg)

    def test_password_invalid_chars(self):
        ok, msg = self.validator.validate("testuser", "Password123!", "Password123!")
        self.assertFalse(ok)
        self.assertIn("недопустимые символы", msg)

    def test_password_types(self):
        ok, msg = self.validator.validate("testuser", 1234567, 1234567)  # type: ignore
        self.assertFalse(ok)
        self.assertIn("строками", msg)

    def test_password_valid_cyrillic(self):
        ok, msg = self.validator.validate("testuser", "Пароль123!", "Пароль123!")
        self.assertTrue(ok)
        self.assertEqual(msg, "")


if __name__ == "__main__":
    unittest.main()
