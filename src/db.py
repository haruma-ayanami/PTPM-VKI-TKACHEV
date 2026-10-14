import sqlite3
from typing import Optional

from .validator import mask_password


class RegistrationDB:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL,
                    confirm_password TEXT NOT NULL,
                    auth_result INTEGER NOT NULL,
                    error_message TEXT
                )
                """
            )
            # Уникальный индекс по ключу идентификации
            self.conn.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_reg_key
                ON registrations (login, password, confirm_password)
                """
            )

    @staticmethod
    def _key(login: str, password: str, confirm: str) -> tuple[str, str, str]:
        # Пароли в БД хранятся только в замаскированном виде
        return login, mask_password(password), mask_password(confirm)

    def add(
        self,
        login: str,
        password: str,
        confirm: str,
        result: bool,
        error_msg: str = "",
    ) -> None:
        key = self._key(login, password, confirm)
        with self.conn:
            self.conn.execute(
                """
                INSERT OR IGNORE INTO registrations
                (login, password, confirm_password, auth_result, error_message)
                VALUES (?, ?, ?, ?, ?)
                """,
                (*key, 1 if result else 0, error_msg or ""),
            )

    def get(
        self,
        login: str,
        password: str,
        confirm: str,
    ) -> Optional[dict]:
        key = self._key(login, password, confirm)
        cur = self.conn.execute(
            """
            SELECT login, password, confirm_password, auth_result, error_message
            FROM registrations
            WHERE login = ? AND password = ? AND confirm_password = ?
            """,
            key,
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {
            "login": row["login"],
            "password": row["password"],
            "confirm_password": row["confirm_password"],
            "auth_result": bool(row["auth_result"]),
            "error_message": row["error_message"] or "",
        }

    def delete(self, login: str, password: str, confirm: str) -> bool:
        key = self._key(login, password, confirm)
        with self.conn:
            cur = self.conn.execute(
                """
                DELETE FROM registrations
                WHERE login = ? AND password = ? AND confirm_password = ?
                """,
                key,
            )
            return cur.rowcount > 0

    def close(self) -> None:
        self.conn.close()
