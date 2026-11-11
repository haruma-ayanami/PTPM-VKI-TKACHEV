"""Загрузка HTML-страницы форума и извлечение сообщений."""

import re

import requests
from bs4 import BeautifulSoup


class ForumParser:
    # Эти селекторы подходят для типовой разметки. Если у сайта другие классы,
    # достаточно добавить их сюда.
    POST_SELECTOR = (
        "[data-post-id], [data-comment-id], [data-message-id], [data-id], "
        "[id*='post'], [id*='comment'], [id*='message'], "
        ".post, .comment, .message, article"
    )
    AUTHOR_SELECTOR = (
        ".username, .user-name, .post-author, .comment-author, "
        ".message-author, .author, .user, [rel='author'], [itemprop='author']"
    )
    MESSAGE_SELECTOR = (
        ".post-content, .post-body, .post-message, .comment-content, "
        ".comment-body, .comment-text, .message-content, .message-body, "
        ".post-text, .content, [itemprop='articleBody'], [itemprop='text']"
    )
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ForumParser/1.0)"}
    ID_PATTERN = re.compile(
        r"(?:post|comment|message)[_-]?(\d+)"
        r"|/(?:posts?|comments?|messages?)/(\d+)"
        r"|#p?(\d+)",
        re.IGNORECASE,
    )

    def __init__(self, timeout=15):
        self.timeout = timeout

    def parse_page(self, url):
        """Скачивает страницу и возвращает список найденных сообщений."""
        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return self.parse_html(response.text)

    def parse_html(self, html):
        """Разбирает HTML-текст; используется и для локальных тестовых страниц."""
        soup = BeautifulSoup(html, "lxml")
        posts_by_id = {}

        # CSS-селектор находит возможные контейнеры сообщений в порядке HTML.
        for post in soup.select(self.POST_SELECTOR):
            comment_id = self._get_id(post)
            author_tag = post.select_one(self.AUTHOR_SELECTOR)
            message_tag = post.select_one(self.MESSAGE_SELECTOR)

            # Если отдельного блока текста нет, берём содержимое самого поста.
            if message_tag is None:
                message_tag = post

            if comment_id is None or author_tag is None:
                continue

            name = author_tag.get_text(" ", strip=True)
            message = message_tag.decode_contents().strip()
            if not name or not message:
                continue

            posts_by_id[comment_id] = {
                "id": comment_id,
                "name": name,
                "message": message,
            }

        # Словарь одновременно убирает дубли и сохраняет порядок страницы.
        return list(posts_by_id.values())

    def save_to_db(self, parsed_data, repository):
        """Передаёт найденные сообщения репозиторию базы данных."""
        if isinstance(parsed_data, dict):
            parsed_data = [parsed_data]

        for post in parsed_data:
            repository.add(post["id"], post["name"], post["message"])
        return True

    def _get_id(self, post):
        """Ищет ID сначала в атрибутах, затем в ссылках внутри поста."""
        tags_to_check = [post] + post.select(
            "[data-post-id], [data-comment-id], [data-message-id], [data-id], [id], a[href]"
        )

        for tag in tags_to_check:
            for attribute in (
                "data-post-id",
                "data-comment-id",
                "data-message-id",
                "data-id",
                "id",
                "href",
            ):
                value = tag.get(attribute)
                if value is None:
                    continue

                value = str(value)
                if value.isdigit():
                    return int(value)

                match = self.ID_PATTERN.search(value)
                if match:
                    number = match.group(1) or match.group(2) or match.group(3)
                    return int(number)

        return None
