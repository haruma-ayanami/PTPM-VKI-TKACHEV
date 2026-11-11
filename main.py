"""Точка входа для запуска парсера из терминала."""

from datetime import datetime
from pathlib import Path

import requests

from src.database import DatabaseRepository
from src.parser import ForumParser


def main():
    url = input("Введите URL страницы форума: ").strip()
    if not url:
        print("URL не указан.")
        return

    parser = ForumParser()
    database_name = datetime.now().strftime("comments_%Y%m%d_%H%M%S_%f.db")
    database_dir = Path(__file__).parent / "db"
    database_dir.mkdir(exist_ok=True)
    database_path = database_dir / database_name
    snapshot_path = Path(__file__).parent / "tests" / "fixtures" / "downloaded_page.html"

    try:
        posts = parser.parse_page(url, save_html_to=snapshot_path)
        print("HTML страницы сохранён в tests/fixtures/downloaded_page.html")
    except requests.RequestException as error:
        print(f"Не удалось загрузить страницу: {error}")
        return

    if not posts:
        print("Сообщения не найдены. Возможно, у сайта другая HTML-разметка.")
        return

    repository = DatabaseRepository(str(database_path))
    try:
        added_count = 0
        skipped_count = 0
        for post in posts:
            try:
                parser.save_to_db([post], repository)
                added_count += 1
            except (TypeError, ValueError) as error:
                skipped_count += 1
                print(f"Запись ID {post['id']} пропущена: {error}")

        for post in posts:
            print(f"ID: {post['id']} | Автор: {post['name']}")
            print(f"Сообщение: {post['message']}\n")

        print(f"Найдено сообщений: {len(posts)}")
        print(f"Добавлено сообщений: {added_count}")
        print(f"Пропущено сообщений: {skipped_count}")
        print(f"База данных сохранена: {database_name}")
    finally:
        repository.close()


if __name__ == "__main__":
    main()
