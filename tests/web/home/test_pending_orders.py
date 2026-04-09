"""
Home page Pending Orders widget tests.

Validates that the Pending Orders widget title and container
are visible on the Home page dashboard.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomePage


@pytest.mark.usefixtures("driver")
class TestPendingOrders:
    """
    Verify Pending Orders widget on the Home page.

    Usage:
        pytest tests/web/home/test_pending_orders.py -v
    """

    def test_c70237_verify_pending_orders_widget_visible(self, driver):
        """C70237 Verify Pending Orders widget is visible."""
        home_page = HomePage(driver)

        assert home_page.text_is_visible("Pending Orders"), (
            "Pending Orders widget title should be visible on the Home page"
        )

        # Verify the widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Pending Orders')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Pending Orders widget container should be visible"
        )
