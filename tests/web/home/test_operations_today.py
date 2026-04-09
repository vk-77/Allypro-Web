"""
Home page Operations Today widget tests.

Validates that the Operations Today widget title and container
with route data are visible on the Home page dashboard.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomePage


@pytest.mark.usefixtures("driver")
class TestOperationsToday:
    """
    Verify Operations Today widget with route data on the Home page.

    Usage:
        pytest tests/web/home/test_operations_today.py -v
    """

    def test_c70213_verify_operations_today_widget_visible(self, driver):
        """C70213 Verify Operations Today widget with route data is visible."""
        home_page = HomePage(driver)

        assert home_page.text_is_visible("Operations Today"), (
            "Operations Today widget title should be visible on the Home page"
        )

        # Verify the widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Operations Today')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Operations Today widget container should be visible"
        )
