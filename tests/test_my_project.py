import unittest

from validation import (
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
        result = mask_password("Пароль1!")
        self.assertEqual(len(result), 16)

    def test_mask_password_returns_same_result_for_same_password(self):
        result1 = mask_password("Пароль1!")
        result2 = mask_password("Пароль1!")
        self.assertEqual(result1, result2)

    def test_mask_password_returns_different_result_for_different_passwords(self):
        result1 = mask_password("Пароль1!")
        result2 = mask_password("Пароль2!")
        self.assertNotEqual(result1, result2)


class TestValidateLogin(unittest.TestCase):

    def test_validate_login_accepts_regular_login(self):
        result = validate_login("user_123")
        self.assertEqual(result, (True, ""))

    def test_validate_login_accepts_phone(self):
        result = validate_login("+7-999-123-4567")
        self.assertEqual(result, (True, ""))

    def test_validate_login_accepts_email(self):
        result = validate_login("user@example.com")
        self.assertEqual(result, (True, ""))

    def test_validate_login_rejects_empty_login(self):
        result = validate_login("")
        self.assertEqual(
            result,
            (False, "Логин не может быть пустым")
        )

    def test_validate_login_rejects_short_login(self):
        result = validate_login("abc")
        self.assertEqual(
            result,
            (False, "Длина логина должна быть минимум 5 символов")
        )

    def test_validate_login_rejects_invalid_symbols(self):
        result = validate_login("user-name")
        self.assertEqual(
            result,
            (
                False,
                "Логин должен содержать только латиницу, "
                "цифры и знак подчеркивания"
            )
        )

    def test_validate_login_rejects_blacklisted_login(self):
        result = validate_login("admin")
        self.assertEqual(
            result,
            (False, "Логин в черном списке")
        )

    def test_validate_login_rejects_non_string_value(self):
        result = validate_login(12345)
        self.assertEqual(
            result,
            (False, "Логин должен быть строкой")
        )


class TestValidatePassword(unittest.TestCase):

    def test_validate_password_accepts_correct_password(self):
        result = validate_password("Пароль1!", "Пароль1!")
        self.assertEqual(result, (True, ""))

    def test_validate_password_rejects_short_password(self):
        result = validate_password("Пар1!", "Пар1!")
        self.assertEqual(
            result,
            (False, "Пароль должен содержать минимум 7 символов")
        )

    def test_validate_password_rejects_different_confirmation(self):
        result = validate_password("Пароль1!", "Пароль2!")
        self.assertEqual(
            result,
            (False, "Пароли не совпадают")
        )

    def test_validate_password_rejects_missing_lowercase(self):
        result = validate_password("ПАРОЛЬ1!", "ПАРОЛЬ1!")
        self.assertEqual(
            result,
            (False, "Нет буквы в нижнем регистре")
        )

    def test_validate_password_rejects_missing_uppercase(self):
        result = validate_password("пароль1!", "пароль1!")
        self.assertEqual(
            result,
            (False, "Нет буквы в верхнем регистре")
        )

    def test_validate_password_rejects_missing_digit(self):
        result = validate_password("Пароль!!", "Пароль!!")
        self.assertEqual(
            result,
            (False, "Нет цифры")
        )

    def test_validate_password_rejects_missing_special_symbol(self):
        result = validate_password("Пароль12", "Пароль12")
        self.assertEqual(
            result,
            (False, "Нет спецсимвола")
        )

    def test_validate_password_rejects_invalid_symbol(self):
        result = validate_password("Пароль1!@", "Пароль1!@")
        self.assertEqual(result, (True, ""))

    def test_validate_password_rejects_non_string_password(self):
        result = validate_password(1234567, "1234567")
        self.assertEqual(
            result,
            (False, "Пароль и подтверждение должны быть строками")
        )

    def test_validate_password_rejects_non_string_confirmation(self):
        result = validate_password("Пароль1!", 1234567)
        self.assertEqual(
            result,
            (False, "Пароль и подтверждение должны быть строками")
        )


class TestRegister(unittest.TestCase):

    def test_register_returns_success_for_valid_data(self):
        result = register(
            "student_123",
            "Пароль1!",
            "Пароль1!"
        )
        self.assertEqual(result, (True, ""))

    def test_register_returns_login_error_for_invalid_login(self):
        result = register(
            "abc",
            "Пароль1!",
            "Пароль1!"
        )
        self.assertEqual(
            result,
            (False, "Длина логина должна быть минимум 5 символов")
        )

    def test_register_returns_password_error_for_invalid_password(self):
        result = register(
            "student_123",
            "пароль1!",
            "пароль1!"
        )
        self.assertEqual(
            result,
            (False, "Нет буквы в верхнем регистре")
        )


if __name__ == "__main__":
    unittest.main()