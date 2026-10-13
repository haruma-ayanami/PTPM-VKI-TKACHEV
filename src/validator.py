import re
import hashlib
import json
import os

BLACKLIST_PATH = os.path.join(os.path.dirname(__file__), "blacklist_login.json")

with open(BLACKLIST_PATH, "r", encoding="utf-8") as f:
    BLACKLIST_LOGIN = json.load(f)

PHONE_PATTERN = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")
LOGIN_STRING_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
SPECIAL_SYMBOLS = set("!@#$%^&*()-_=+[]{};:,.?")
CYRILLIC_LOWER = set(
    chr(c) for c in range(ord("а"), ord("я") + 1)
) | {"ё"}
CYRILLIC_UPPER = set(
    chr(c) for c in range(ord("А"), ord("Я") + 1)
) | {"Ё"}
CYRILLIC = CYRILLIC_LOWER | CYRILLIC_UPPER


def is_cyrillic(c: str) -> bool:
    return c in CYRILLIC


def mask_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()[:16]


def validate_login(login: str) -> tuple[bool, str]:
    if not isinstance(login, str):
        return False, "Логин должен быть строкой"

    if not login:
        return False, "Логин не может быть пустым"

    if login in BLACKLIST_LOGIN:
        return False, "Логин в черном списке"

    if PHONE_PATTERN.match(login):
        return True, ""

    if EMAIL_PATTERN.match(login):
        return True, ""

    if len(login) < 5:
        return False, "Длина логина должна быть минимум 5 символов"

    if not LOGIN_STRING_PATTERN.match(login):
        return False, "Логин должен содержать только латиницу, цифры и знак подчеркивания"

    return True, ""


def validate_password(password: str, confirm: str) -> tuple[bool, str]:
    if not isinstance(password, str) or not isinstance(confirm, str):
        return False, "Пароль и подтверждение должны быть строками"

    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    if password != confirm:
        return False, "Пароли не совпадают"

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for c in password:
        if c.isdigit():
            has_digit = True

        elif c in SPECIAL_SYMBOLS:
            has_special = True

        elif is_cyrillic(c):
            if c.islower():
                has_lower = True

            if c.isupper():
                has_upper = True

        else:
            return False, "Пароль содержит недопустимые символы"

    if not has_lower:
        return False, "Нет буквы в нижнем регистре"

    if not has_upper:
        return False, "Нет буквы в верхнем регистре"

    if not has_digit:
        return False, "Нет цифры"

    if not has_special:
        return False, "Нет спецсимвола"

    return True, ""


class AuthValidator:
    def validate(self, login: str, password: str, confirm: str) -> tuple[bool, str]:
        ok_login, msg_login = validate_login(login)
        if not ok_login:
            return False, msg_login

        result = validate_password(password, confirm)
        return result

    def mask_password(self, password: str) -> str:
        return mask_password(password)
