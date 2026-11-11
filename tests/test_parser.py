from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from src.database import DatabaseRepository
from src.parser import ForumParser


FIXTURE = Path(__file__).parent / "fixtures" / "forum_page.html"


class ForumParserTests(unittest.TestCase):
    def setUp(self):
        self.html = FIXTURE.read_text(encoding="utf-8")
        self.parser = ForumParser()

    @patch("src.parser.requests.get")
    def test_parse_page_extracts_posts_from_saved_html_fixture(self, get):
        response = Mock()
        response.text = self.html
        get.return_value = response

        result = self.parser.parse_page("https://forum.example/topic/1")

        self.assertEqual(
            result,
            [
                {
                    "id": 4812,
                    "name": "alex_dev",
                    "message": "<p>Hello <strong>forum</strong>!</p>",
                },
                {
                    "id": 4813,
                    "name": "maria",
                    "message": "A second <em>reply</em>.",
                },
            ],
        )
        response.raise_for_status.assert_called_once_with()
        self.assertIn("User-Agent", get.call_args.kwargs["headers"])

    @patch("src.parser.requests.get")
    def test_save_to_db_stores_parsed_posts(self, get):
        response = Mock()
        response.text = self.html
        get.return_value = response
        records = self.parser.parse_page("https://forum.example/topic/1")
        repository = DatabaseRepository(":memory:")
        self.addCleanup(repository.close)

        self.assertTrue(self.parser.save_to_db(records, repository))
        self.assertEqual(repository.get_by_id(4812)["name"], "alex_dev")
        self.assertEqual(repository.get_by_id(4813)["name"], "maria")

    def test_parse_html_skips_records_without_author_or_message(self):
        html = '<article id="post_9"><div class="post-content">body</div></article>'
        self.assertEqual(self.parser.parse_html(html), [])


if __name__ == "__main__":
    unittest.main()
