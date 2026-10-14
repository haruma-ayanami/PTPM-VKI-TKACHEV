import unittest

from src.interfaces import AbstractExternalService, AbstractUserInterface


class TestInterfaces(unittest.TestCase):
    def test_interfaces_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            AbstractUserInterface()
        with self.assertRaises(TypeError):
            AbstractExternalService()

    def test_base_methods_are_placeholders(self):
        # Тела абстрактных методов вызываются только через super() в наследнике
        class UI(AbstractUserInterface):
            def get_credentials(self):
                return super().get_credentials()

        class External(AbstractExternalService):
            def send(self, result):
                return super().send(result)

        self.assertIsNone(UI().get_credentials())
        self.assertIsNone(External().send("x"))


if __name__ == "__main__":
    unittest.main()
