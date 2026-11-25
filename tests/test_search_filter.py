"""UI tests for the GlobalSQA Search Filter demo."""

import os
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.search_filter_page import SearchFilterPage


class SearchFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        browser_name = os.environ.get("BROWSER", "edge").lower()
        if browser_name == "chrome":
            options = Options()
            browser_factory = webdriver.Chrome
        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            browser_factory = webdriver.Edge
        else:
            self.fail("BROWSER must be either 'chrome' or 'edge'.")

        options.page_load_strategy = "eager"
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        self.driver = browser_factory(options=options)
        self.driver.set_page_load_timeout(20)
        self.page = SearchFilterPage(self.driver).open()

    def tearDown(self) -> None:
        driver = getattr(self, "driver", None)
        if driver is not None:
            driver.quit()

    def test_payee_filter_returns_matching_transactions(self) -> None:
        results = self.page.search_by_payee("InternetBill").wait_for_result_count(2)

        self.assertEqual([row["payee"] for row in results], ["InternetBill", "InternetBill"])

    def test_expenditure_payee_filter_returns_matching_transactions(self) -> None:
        results = self.page.search_by_expenditure_payee("PowerBill").wait_for_result_count(1)

        self.assertEqual([row["payee"] for row in results], ["PowerBill"])
        self.assertEqual([row["type"] for row in results], ["EXPENDITURE"])

    def test_account_filter_returns_matching_transactions(self) -> None:
        results = self.page.select_account("Bank Savings").wait_for_result_count(2)

        self.assertEqual(
            [row["account"] for row in results],
            ["Bank Savings", "Bank Savings"],
        )

    def test_type_filter_returns_matching_transactions(self) -> None:
        results = self.page.select_type("INCOME").wait_for_result_count(1)

        self.assertEqual([row["payee"] for row in results], ["Salary"])
        self.assertEqual([row["type"] for row in results], ["INCOME"])

    def test_filters_can_be_combined(self) -> None:
        results = (
            self.page.select_account("Cash")
            .select_type("EXPENDITURE")
            .search_by_payee("InternetBill")
            .wait_for_result_count(1)
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            (
                results[0]["account"],
                results[0]["type"],
                results[0]["payee"],
                results[0]["amount"],
            ),
            ("Cash", "EXPENDITURE", "InternetBill", "1200"),
        )

    def test_clearing_filters_restores_all_transactions(self) -> None:
        self.page.search_by_payee("InternetBill").select_account("Bank Savings")
        self.page.wait_for_result_count(1)

        results = self.page.clear_filters().wait_for_result_count(5)

        self.assertEqual(len(results), 5)
        self.assertEqual(self.page.selected_account(), "All Accounts")
        self.assertEqual(self.page.selected_type(), "All Types")

    def test_search_with_no_matches_returns_empty_results(self) -> None:
        results = self.page.search_by_payee("NoSuchPayee").wait_for_result_count(0)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
