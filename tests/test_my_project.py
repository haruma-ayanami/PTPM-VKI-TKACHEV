import unittest

from src.my_project import (
    is_cyrillic,
    mask_password,
    validate_login,
    validate_password,
    register,
)


class TestCyrillic(unittest.TestCase):

    def test_is_cyrillic_returns_true_for_lowercase_letter(self):
        self.assertTrue(is_cyrillic("а"))

    def test_is_cyrillic_returns_true_for_uppercase_letter(self):
        self.assertTrue(is_cyrillic("Я"))

    def test_is_cyrillic_returns_true_for_yo(self):
        self.assertTrue(is_cyrillic("ё"))

    def test_is_cyrillic_returns_false_for_latin_letter(self):
        self.assertFalse(is_cyrillic("a"))

    def test_is_cyrillic_returns_false_for_digit(self):
        self.assertFalse(is_cyrillic("5"))


class TestMaskPassword(unittest.TestCase):

    def test_mask_password_returns_16_characters(self):
        self.assertEqual(len(mask_password("Пароль1!")), 16)

    def test_mask_password_returns_same_result_for_same_password(self):
        self.assertEqual(mask_password("Пароль1!"), mask_password("Пароль1!"))

    def test_mask_password_returns_different_result_for_different_passwords(self):
        self.assertNotEqual(mask_password("Пароль1!"), mask_password("Пароль2!"))


class TestValidateLogin(unittest.TestCase):

    def test_validate_login_accepts_regular_login(self):
        self.assertEqual(validate_login("user_123"), (True, ""))

    def test_validate_login_accepts_phone(self):
        self.assertEqual(validate_login("+7-999-123-4567"), (True, ""))

    def test_validate_login_accepts_email(self):
        self.assertEqual(validate_login("user@example.com"), (True, ""))

    def test_validate_login_rejects_empty_login(self):
        self.assertEqual(validate_login(""), (False, "Логин не может быть пустым"))

    def test_validate_login_rejects_short_login(self):
        self.assertEqual(
            validate_login("abc"),
            (False, "Длина логина должна быть минимум 5 символов")
        )

    def test_validate_login_rejects_invalid_symbols(self):
        # дефис не входит в разрешённый набор латиница, цифры, подчёркивание
        self.assertEqual(
            validate_login("user-name"),
            (False, "Логин должен содержать только латиницу, цифры и знак подчеркивания")
        )

    def test_validate_login_rejects_blacklisted_login(self):
        self.assertEqual(validate_login("admin"), (False, "Логин в черном списке"))

    def test_validate_login_rejects_non_string_value(self):
        self.assertEqual(validate_login(12345), (False, "Логин должен быть строкой"))


class TestValidatePassword(unittest.TestCase):

    def test_validate_password_accepts_correct_password(self):
        self.assertEqual(validate_password("Пароль1!", "Пароль1!"), (True, ""))

    def test_validate_password_rejects_short_password(self):
        self.assertEqual(
            validate_password("Пар1!", "Пар1!"),
            (False, "Пароль должен содержать минимум 7 символов")
        )

    def test_validate_password_rejects_different_confirmation(self):
        self.assertEqual(
            validate_password("Пароль1!", "Пароль2!"),
            (False, "Пароли не совпадают")
        )

    def test_validate_password_rejects_missing_lowercase(self):
        self.assertEqual(
            validate_password("ПАРОЛЬ1!", "ПАРОЛЬ1!"),
            (False, "Нет буквы в нижнем регистре")
        )

    def test_validate_password_rejects_missing_uppercase(self):
        self.assertEqual(
            validate_password("пароль1!", "пароль1!"),
            (False, "Нет буквы в верхнем регистре")
        )

    def test_validate_password_rejects_missing_digit(self):
        self.assertEqual(
            validate_password("Пароль!!", "Пароль!!"),
            (False, "Нет цифры")
        )

    def test_validate_password_rejects_missing_special_symbol(self):
        self.assertEqual(
            validate_password("Пароль12", "Пароль12"),
            (False, "Нет спецсимвола")
        )

    def test_validate_password_accepts_multiple_special_symbols(self):
        # спецсимволов может быть сколько угодно, главное чтоб был хотя бы один
        self.assertEqual(validate_password("Пароль1!@", "Пароль1!@"), (True, ""))

    def test_validate_password_rejects_non_string_password(self):
        self.assertEqual(
            validate_password(1234567, "1234567"),
            (False, "Пароль и подтверждение должны быть строками")
        )

    def test_validate_password_rejects_non_string_confirmation(self):
        self.assertEqual(
            validate_password("Пароль1!", 1234567),
            (False, "Пароль и подтверждение должны быть строками")
        )


class TestRegister(unittest.TestCase):

    def test_register_returns_success_for_valid_data(self):
        self.assertEqual(register("student_123", "Пароль1!", "Пароль1!"), (True, ""))

    def test_register_returns_login_error_for_invalid_login(self):
        self.assertEqual(
            register("abc", "Пароль1!", "Пароль1!"),
            (False, "Длина логина должна быть минимум 5 символов")
        )

    def test_register_returns_password_error_for_invalid_password(self):
        self.assertEqual(
            register("student_123", "пароль1!", "пароль1!"),
            (False, "Нет буквы в верхнем регистре")
        )


if __name__ == "__main__":
    unittest.main()
