import logging
import unittest
from unittest.mock import patch

from src.logger import setup_logging


class TestSetupLogging(unittest.TestCase):
    # logging.info() сам вызывает basicConfig, если у корня нет обработчиков, поэтому глушим и его
    @patch("src.logger.logging.info")
    @patch("src.logger.logging.basicConfig")
    @patch("src.logger.logging.FileHandler")
    @patch("src.logger.os.makedirs")
    def test_configures_root_logger(self, makedirs, file_handler, basic_config, info):
        setup_logging()

        makedirs.assert_called_once_with("logs", exist_ok=True)
        file_handler.assert_called_once_with("logs/file_txt.log", encoding="utf-8")
        basic_config.assert_called_once()
        kwargs = basic_config.call_args.kwargs
        self.assertEqual(kwargs["level"], logging.DEBUG)
        self.assertEqual(len(kwargs["handlers"]), 2)


if __name__ == "__main__":
    unittest.main()
