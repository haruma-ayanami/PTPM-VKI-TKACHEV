# Лабораторная работа: UI-тестирование с Page Object Model

Проект содержит автоматизированные UI-тесты для приложения [Search Filter](https://www.globalsqa.com/angularJs-protractor/SearchFilter/) с использованием Python, Selenium WebDriver и `unittest`.

Класс страницы в `pages/` хранит локаторы и предоставляет методы для поиска по Payee, Account и Type, сброса фильтров и чтения результатов. Тесты работают только через методы Page Object.

## Установка и запуск

Требуются Python 3 и установленный Chromium-based Microsoft Edge или Google Chrome. По умолчанию тесты запускаются в Edge; Selenium Manager подбирает WebDriver при запуске. Для Chrome задайте `BROWSER=chrome`.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Для Chrome задайте переменную окружения перед запуском: `BROWSER=chrome python -m unittest discover -s tests -v`.

Тесты создают отдельную сессию браузера в `setUp()` и закрывают её в `tearDown()`.
