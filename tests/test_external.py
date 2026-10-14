import unittest

from src.external import DummyExternalService
from src.interfaces import AbstractExternalService


class TestDummyExternalService(unittest.TestCase):
    def test_implements_interface(self):
        self.assertIsInstance(DummyExternalService(), AbstractExternalService)

    def test_send_logs_result(self):
        service = DummyExternalService()
        result = "success: True, message: Регистрация прошла успешно"

        with self.assertLogs(level="INFO") as logs:
            service.send(result)

        self.assertEqual(len(logs.records), 1)
        self.assertIn(result, logs.output[0])


if __name__ == "__main__":
    unittest.main()
