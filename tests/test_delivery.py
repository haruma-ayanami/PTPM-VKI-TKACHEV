import unittest

from delivery import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    def test_rejects_weight_less_than_minimum(self):
        result = calculate_delivery_cost(
            0.09, 100, "обычный"
        )
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_accepts_minimum_weight(self):
        result = calculate_delivery_cost(
            0.1, 100, "обычный"
        )
        self.assertEqual(result, (700, "2026-09-03"))

    def test_rejects_weight_greater_than_maximum(self):
        result = calculate_delivery_cost(
            50.1, 100, "обычный"
        )
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_accepts_maximum_weight(self):
        result = calculate_delivery_cost(
            50.0, 100, "обычный"
        )
        self.assertEqual(result, (1050, "2026-09-03"))

    def test_rejects_distance_less_than_minimum(self):
        result = calculate_delivery_cost(
            1, 0, "обычный"
        )
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_distance_greater_than_maximum(self):
        result = calculate_delivery_cost(
            1, 5001, "обычный"
        )
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_invalid_package_type(self):
        result = calculate_delivery_cost(
            1, 100, "электроника"
        )
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_calculates_regular_package_cost(self):
        result = calculate_delivery_cost(
            5, 100, "обычный"
        )
        self.assertEqual(result, (700, "2026-09-03"))

    def test_applies_medium_weight_coefficient(self):
        result = calculate_delivery_cost(
            10, 100, "обычный"
        )
        self.assertEqual(result, (840, "2026-09-03"))

    def test_applies_heavy_weight_coefficient(self):
        result = calculate_delivery_cost(
            20, 100, "обычный"
        )
        self.assertEqual(result, (1050, "2026-09-03"))

    def test_adds_fragile_package_fee(self):
        result = calculate_delivery_cost(
            1, 100, "хрупкий"
        )
        self.assertEqual(result, (1000, "2026-09-03"))

    def test_adds_dangerous_package_fee(self):
        result = calculate_delivery_cost(
            1, 100, "опасный"
        )
        self.assertEqual(result, (1700, "2026-09-03"))

    def test_calculates_delivery_date_for_long_distance(self):
        result = calculate_delivery_cost(
            1, 1000, "обычный"
        )
        self.assertEqual(result, (5200, "2026-09-05"))

    def test_express_delivery_reduces_delivery_time(self):
        result = calculate_delivery_cost(
            1, 1000, "обычный", True
        )
        self.assertEqual(result, (2600, "2026-09-04"))

    def test_express_delivery_has_at_least_one_delivery_day(self):
        result = calculate_delivery_cost(
            1, 500, "обычный", True
        )
        self.assertEqual(result, (1350, "2026-09-04"))


if __name__ == "__main__":
    unittest.main()