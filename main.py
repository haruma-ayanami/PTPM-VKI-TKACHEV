"""Точка входа для запуска парсера из терминала."""

import requests

from src.database import DatabaseRepository
from src.parser import ForumParser


def main():
    url = input("Введите URL страницы форума: ").strip()
    if not url:
        print("URL не указан.")
        return

    parser = ForumParser()
    repository = DatabaseRepository("comments.db")

    try:
        posts = parser.parse_page(url)

        if not posts:
            print("Сообщения не найдены. Возможно, у сайта другая HTML-разметка.")
            return

        # При повторном запуске пропускаем ID, которые уже есть в базе.
        new_posts = [
            post for post in posts
            if repository.get_by_id(post["id"]) is None
        ]
        parser.save_to_db(new_posts, repository)

        for post in posts:
            print(f"ID: {post['id']} | Автор: {post['name']}")
            print(f"Сообщение: {post['message']}\n")

        print(f"Найдено сообщений: {len(posts)}")
        print(f"Добавлено в comments.db: {len(new_posts)}")
    except requests.RequestException as error:
        print(f"Не удалось загрузить страницу: {error}")
    finally:
        repository.close()


if __name__ == "__main__":
    main()
