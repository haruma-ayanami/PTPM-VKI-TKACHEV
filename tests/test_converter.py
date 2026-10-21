import unittest

from src.converter import Converter


class TestConverter(unittest.TestCase):
    def test_upper_range_returns_1000(self):
        self.assertEqual(Converter.do(100.7), 1000)
        self.assertEqual(Converter.do(150.0), 1000)
        self.assertEqual(Converter.do(1000000.0), 1000)

    def test_positive_range_truncates_fraction(self):
        self.assertEqual(Converter.do(0.1), 0)
        self.assertEqual(Converter.do(50.9), 50)
        self.assertEqual(Converter.do(100.6), 100)

    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_negative_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(-0.0)

    def test_negative_range_truncates_and_subtracts_5(self):
        self.assertEqual(Converter.do(-0.1), -5)
        self.assertEqual(Converter.do(-1.5), -6)
        self.assertEqual(Converter.do(-30.4), -35)

    def test_lower_range_returns_minus_2000(self):
        self.assertEqual(Converter.do(-30.5), -2000)
        self.assertEqual(Converter.do(-30.6), -2000)
        self.assertEqual(Converter.do(-1000.0), -2000)
