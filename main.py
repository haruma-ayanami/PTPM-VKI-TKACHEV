import re
import hashlib
import logging
import json
from logger import setup_logging

with open("blacklist_login.json", "r", encoding="utf-8") as f:
    BLACKLIST_LOGIN = json.load(f)
PHONE_PATTERN = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")
LOGIN_STRING_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
SPECIAL_SYMBOLS = set("!@#$%^&*()-_=+[]{};:,.?")
CYRILLIC_LOWER = set(chr(c) for c in range(ord("а"), ord("я") + 1)) | {"ё"}
CYRILLIC_UPPER = set(chr(c) for c in range(ord("А"), ord("Я") + 1)) | {"Ё"}
CYRILLIC = CYRILLIC_LOWER | CYRILLIC_UPPER

def is_cyrillic(c: str) -> bool:
    return c in CYRILLIC

def mask_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()[:16]

def validate_login(login: str) -> tuple[bool, str]:
    if not login:
        return False, "Логин не может быть пустым"

    if login in BLACKLIST_LOGIN:
        return False, "Логин в черном списке"

    if PHONE_PATTERN.match(login) or EMAIL_PATTERN.match(login):
        return True, ""

    if len(login) < 5:
        return False, "Длина логина должна быть больше 5 символов"

    if not LOGIN_STRING_PATTERN.match(login):
        return False, "Логин должен содержать только латиницу, цифры и знак подчеркивания"

    return True, ""

def validate_password(password: str, confirm: str) -> tuple[bool, str]:
    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    if password != confirm:
        return False, "Пароли не совпадают"

    has_lower = has_upper = has_digit = has_special = False
    valid_symbols = True

    for c in password:
        if c.isdigit():
            has_digit = True
        elif c in SPECIAL_SYMBOLS:
            has_special = True
        elif is_cyrillic(c):
            has_lower = has_lower or c.islower()
            has_upper = has_upper or c.isupper()
        else:
            valid_symbols = False

    if not valid_symbols:
        return False, "Пароль содержит недоступные символы (только кириллица)"
    if not has_lower:
        return False, "Нет буквы в нижнем регистре"
    if not has_upper:
        return False, "Нет буквы в верхнем регистре"
    if not has_digit:
        return False, "Нет цифры"
    if not has_special:
        return False, "Нет спецсимвола"

    return True, ""

def register(login: str, password: str, confirm: str) -> tuple[bool, str]:
    masked = mask_password(password)
    logging.info(f"Запрос на регистрацию: логин={login}, пароль={masked}")

    ok_login, msg_login = validate_login(login)
    if not ok_login:
        logging.warning(f"Ошибка валидации логина: {msg_login}")
        return False, msg_login

    result = validate_password(password, confirm)

    if result[0]:
        logging.info(f"Регистрация успешна: логин={login}")
    else:
        logging.warning(f"Ошибка валидации пароля: {result[1]}")

    return result

def main() -> None:
    setup_logging()

    while True:
        login = input("Введите логин (телефон или email): ")
        password = input("Введите пароль: ")
        password_confirm = input("Повторите пароль: ")

        try:
            success, message = register(login, password, password_confirm)
        except TypeError:
            logging.exception("Ошибка: Некорректные данные")
            print("Ошибка: Некорректные данные. Пожалуйста, введите строковые значения.")
            continue
        except Exception:
            logging.exception("Непредвиденная ошибка при регистрации")
            print("Произошла непредвиденная ошибка. Проверьте логи.")
            continue

        if not success:
            print(f"Ошибка: {message}")
            continue

        break

if __name__ == "__main__":
    main()
