import sqlite3
import unittest

from src.database import DatabaseRepository


class DatabaseRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repository = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repository.close()

    def test_add_saves_a_comment(self):
        self.assertTrue(self.repository.add(1, "alice", "<p>Hello</p>"))
        self.assertEqual(
            self.repository.get_by_id(1),
            {"id": 1, "name": "alice", "message": "<p>Hello</p>"},
        )

    def test_add_rejects_duplicate_id(self):
        self.repository.add(1, "alice", "first")
        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.add(1, "bob", "duplicate")

    def test_get_by_id_returns_none_when_missing(self):
        self.assertIsNone(self.repository.get_by_id(404))

    def test_get_by_id_returns_matching_comment(self):
        self.repository.add(7, "alice", "hello")
        self.assertEqual(self.repository.get_by_id(7)["name"], "alice")

    def test_get_by_name_returns_all_matching_comments_in_id_order(self):
        self.repository.add(8, "alice", "second")
        self.repository.add(3, "alice", "first")
        self.repository.add(4, "bob", "other")
        self.assertEqual(
            [comment["id"] for comment in self.repository.get_by_name("alice")],
            [3, 8],
        )

    def test_get_by_name_returns_empty_list_when_missing(self):
        self.assertEqual(self.repository.get_by_name("unknown"), [])

    def test_update_changes_existing_comment(self):
        self.repository.add(2, "alice", "old")
        self.assertTrue(self.repository.update(2, "new"))
        self.assertEqual(self.repository.get_by_id(2)["message"], "new")

    def test_update_returns_false_for_missing_comment(self):
        self.assertFalse(self.repository.update(404, "new"))

    def test_delete_removes_existing_comment(self):
        self.repository.add(5, "alice", "remove me")
        self.assertTrue(self.repository.delete(5))
        self.assertIsNone(self.repository.get_by_id(5))

    def test_delete_returns_false_for_missing_comment(self):
        self.assertFalse(self.repository.delete(404))

    def test_add_validates_text_lengths_and_types(self):
        with self.assertRaises(ValueError):
            self.repository.add(1, "a" * 257, "valid")
        with self.assertRaises(ValueError):
            self.repository.add(1, "alice", "m" * 8097)
        with self.assertRaises(TypeError):
            self.repository.add(1, None, "valid")

    def test_update_validates_message_length(self):
        with self.assertRaises(ValueError):
            self.repository.update(1, "m" * 8097)


if __name__ == "__main__":
    unittest.main()
