"""Page Object for the GlobalSQA AngularJS Search Filter demo."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class SearchFilterPage:
    """Encapsulate the Search Filter controls and their result table."""

    URL = "https://www.globalsqa.com/angularJs-protractor/SearchFilter/"

    _PAYEE_INPUT = (By.ID, "input1")
    _ACCOUNT_SELECT = (By.ID, "input2")
    _TYPE_SELECT = (By.ID, "input3")
    _EXPENDITURE_PAYEE_INPUT = (By.ID, "input4")
    _RESULT_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    _RESULT_COLUMNS = ("number", "account", "type", "payee", "amount")

    def __init__(self, driver, timeout: int = 10) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)

    def open(self) -> SearchFilterPage:
        """Load the demo and wait for its initial five transactions."""
        self._driver.get(self.URL)
        self._wait.until(EC.visibility_of_element_located(self._PAYEE_INPUT))
        self._wait.until(EC.visibility_of_element_located(self._ACCOUNT_SELECT))
        self._wait.until(EC.visibility_of_element_located(self._TYPE_SELECT))
        self.wait_for_result_count(5)
        return self

    def search_by_payee(self, payee: str) -> SearchFilterPage:
        self._replace_text(self._PAYEE_INPUT, payee)
        return self

    def search_by_expenditure_payee(self, payee: str) -> SearchFilterPage:
        self._replace_text(self._EXPENDITURE_PAYEE_INPUT, payee)
        return self

    def select_account(self, account: str) -> SearchFilterPage:
        Select(self._visible_element(self._ACCOUNT_SELECT)).select_by_visible_text(account)
        return self

    def select_type(self, transaction_type: str) -> SearchFilterPage:
        Select(self._visible_element(self._TYPE_SELECT)).select_by_visible_text(
            transaction_type
        )
        return self

    def clear_filters(self) -> SearchFilterPage:
        """Restore every search control to its initial state."""
        self._replace_text(self._PAYEE_INPUT, "")
        self._replace_text(self._EXPENDITURE_PAYEE_INPUT, "")
        Select(self._visible_element(self._ACCOUNT_SELECT)).select_by_visible_text(
            "All Accounts"
        )
        Select(self._visible_element(self._TYPE_SELECT)).select_by_visible_text(
            "All Types"
        )
        return self

    def results(self) -> list[dict[str, str]]:
        """Return visible table rows as dictionaries keyed by column name."""
        results = []
        for row in self._driver.find_elements(*self._RESULT_ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == len(self._RESULT_COLUMNS):
                results.append(
                    {
                        column: cell.text.strip()
                        for column, cell in zip(self._RESULT_COLUMNS, cells)
                    }
                )
        return results

    def wait_for_result_count(self, count: int) -> list[dict[str, str]]:
        self._wait.until(lambda _driver: len(self.results()) == count)
        return self.results()

    def selected_account(self) -> str:
        return Select(self._visible_element(self._ACCOUNT_SELECT)).first_selected_option.text

    def selected_type(self) -> str:
        return Select(self._visible_element(self._TYPE_SELECT)).first_selected_option.text

    def _replace_text(self, locator: tuple[str, str], value: str) -> None:
        field = self._visible_element(locator)
        field.clear()
        if value:
            field.send_keys(value)

    def _visible_element(self, locator: tuple[str, str]):
        return self._wait.until(EC.visibility_of_element_located(locator))
