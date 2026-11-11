"""SQLite-хранилище для сообщений форума."""

import sqlite3


class DatabaseRepository:
    """Добавляет, ищет, изменяет и удаляет сообщения в таблице comments."""

    def __init__(self, db_path="comments.db"):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        # Ограничения в таблице защищают данные и при прямой записи в SQLite.
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK (length(name) <= 256),
                message TEXT NOT NULL CHECK (length(message) <= 8096)
            )
            """
        )
        self.connection.commit()

    @staticmethod
    def _check_id(comment_id):
        if type(comment_id) is not int:
            raise TypeError("comment_id должен быть целым числом")

    @staticmethod
    def _check_text(value, field, max_length):
        if not isinstance(value, str):
            raise TypeError(f"{field} должен быть строкой")
        if len(value) > max_length:
            raise ValueError(f"{field}: максимум {max_length} символов")

    def get_by_id(self, comment_id):
        self._check_id(comment_id)
        row = self.connection.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        ).fetchone()
        return dict(row) if row is not None else None

    def get_by_name(self, username):
        self._check_text(username, "username", 256)
        rows = self.connection.execute(
            "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id",
            (username,),
        ).fetchall()
        return [dict(row) for row in rows]

    def add(self, comment_id, username, message):
        self._check_id(comment_id)
        self._check_text(username, "username", 256)
        self._check_text(message, "message", 8096)

        # Знак ? передаёт значения отдельно от SQL-команды.
        with self.connection:
            self.connection.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
        return True

    def update(self, comment_id, new_message):
        self._check_id(comment_id)
        self._check_text(new_message, "new_message", 8096)

        with self.connection:
            cursor = self.connection.execute(
                "UPDATE comments SET message = ? WHERE id = ?",
                (new_message, comment_id),
            )
        return cursor.rowcount > 0

    def delete(self, comment_id):
        """Удаляет сообщение и возвращает True, если оно существовало."""
        self._check_id(comment_id)
        with self.connection:
            cursor = self.connection.execute(
                "DELETE FROM comments WHERE id = ?", (comment_id,)
            )
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
