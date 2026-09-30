import unittest

from src.delivery_service import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    def test_rejects_weight_less_than_minimum(self):
        result = calculate_delivery_cost(0.09, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_accepts_minimum_weight(self):
        result = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-03"))

    def test_rejects_weight_greater_than_maximum(self):
        result = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_accepts_maximum_weight(self):
        # 50 >= 20 -> коэффициент 1.5: (200 + 100 * 5) * 1.5 = 1050
        result = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertEqual(result, (1050, "2026-09-03"))

    def test_rejects_distance_less_than_minimum(self):
        result = calculate_delivery_cost(1, 0, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_distance_greater_than_maximum(self):
        result = calculate_delivery_cost(1, 5001, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_rejects_invalid_package_type(self):
        result = calculate_delivery_cost(1, 100, "электроника")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_calculates_regular_package_cost(self):
        # 5 не попадает в "больше 5" -> коэффициента нет: 200 + 100 * 5 = 700
        result = calculate_delivery_cost(5, 100, "обычный")
        self.assertEqual(result, (700, "2026-09-03"))

    def test_applies_medium_weight_coefficient(self):
        # 5 < 10 < 20 -> коэффициент 1.2: (200 + 100 * 5) * 1.2 = 840
        result = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(result, (840, "2026-09-03"))

    def test_applies_heavy_weight_coefficient(self):
        # 20 >= 20 -> коэффициент 1.5: (200 + 100 * 5) * 1.5 = 1050
        result = calculate_delivery_cost(20, 100, "обычный")
        self.assertEqual(result, (1050, "2026-09-03"))

    def test_adds_fragile_package_fee(self):
        # надбавка 300: 700 + 300 = 1000
        result = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(result, (1000, "2026-09-03"))

    def test_adds_dangerous_package_fee(self):
        # надбавка 1000: 700 + 1000 = 1700
        result = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(result, (1700, "2026-09-03"))

    def test_calculates_delivery_date_for_long_distance(self):
        # 1000 // 500 = 2 дня, 03.09 + 2 = 05.09
        result = calculate_delivery_cost(1, 1000, "обычный")
        self.assertEqual(result, (5200, "2026-09-05"))

    def test_express_delivery_reduces_delivery_time(self):
        # 5200 * 0.5 = 2600, 2 дня // 2 = 1 день -> 04.09
        result = calculate_delivery_cost(1, 1000, "обычный", True)
        self.assertEqual(result, (2600, "2026-09-04"))

    def test_express_delivery_has_at_least_one_delivery_day(self):
        # 1 день // 2 = 0, но экспресс не может быть мгновенным -> ждём 04.09
        result = calculate_delivery_cost(1, 500, "обычный", True)
        self.assertEqual(result, (1350, "2026-09-04"))

    def test_does_not_apply_coefficient_at_five_kg_boundary(self):
        # ровно 5 не попадает в "больше 5" -> 5200 без коэффициента
        result = calculate_delivery_cost(5, 1000, "обычный")
        self.assertEqual(result, (5200, "2026-09-05"))

    def test_applies_medium_coefficient_above_five_kg(self):
        # 5.1 > 5 -> коэффициент 1.2: 5200 * 1.2 = 6240
        result = calculate_delivery_cost(5.1, 1000, "обычный")
        self.assertEqual(result, (6240, "2026-09-05"))

    def test_applies_heavy_coefficient_at_twenty_kg_boundary(self):
        # 20 -> коэффициент 1.5: 5200 * 1.5 = 7800
        result = calculate_delivery_cost(20, 1000, "обычный")
        self.assertEqual(result, (7800, "2026-09-05"))

    def test_calculates_cost_for_maximum_distance(self):
        # 5000 // 500 = 10 дней -> 13.09; 200 + 5000 * 5 = 25200
        result = calculate_delivery_cost(1, 5000, "обычный")
        self.assertEqual(result, (25200, "2026-09-13"))

    def test_adds_dangerous_fee_for_heavy_package(self):
        # коэффициент и надбавка вместе: 5200 * 1.5 + 1000 = 8800
        result = calculate_delivery_cost(25, 1000, "опасный")
        self.assertEqual(result, (8800, "2026-09-05"))

    def test_adds_fragile_fee_for_medium_package(self):
        # коэффициент и надбавка вместе: 5200 * 1.2 + 300 = 6540
        result = calculate_delivery_cost(10, 1000, "хрупкий")
        self.assertEqual(result, (6540, "2026-09-05"))

    def test_calculates_cost_for_minimum_weight_long_distance(self):
        # минимальный вес, коэффициента нет: 200 + 2000 * 5 = 10200
        result = calculate_delivery_cost(0.1, 2000, "обычный")
        self.assertEqual(result, (10200, "2026-09-07"))


if __name__ == "__main__":
    unittest.main()
