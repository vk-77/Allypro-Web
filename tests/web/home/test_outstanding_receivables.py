"""
Home page Outstanding Receivables widget tests.

Validates that the Outstanding Receivables chart widget title and
container are visible on the Home page dashboard.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomePage


@pytest.mark.usefixtures("driver")
class TestOutstandingReceivables:
    """
    Verify Outstanding Receivables chart/widget on the Home page.

    Usage:
        pytest tests/web/home/test_outstanding_receivables.py -v
    """

    def test_c70207_verify_outstanding_receivables_widget_visible(self, driver):
        """C70207 Verify Outstanding Receivables chart/widget is visible."""
        home_page = HomePage(driver)

        assert home_page.text_is_visible("Outstanding Receivables"), (
            "Outstanding Receivables widget title should be visible "
            "on the Home page"
        )

        # Verify the chart/widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Outstanding Receivables')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Outstanding Receivables widget container should be visible"
        )
