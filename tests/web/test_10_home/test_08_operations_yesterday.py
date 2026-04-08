"""
Home - Operations Yesterday widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage


@pytest.mark.usefixtures("driver")
class TestOperationsYesterday:
    """
    Verify Operations Yesterday widget on the Home page.

    Usage:
        pytest tests/web/test_10_home/test_08_operations_yesterday.py -v
    """

    def test_c70220_verify_operations_yesterday_widget_visible(self, driver):
        """C70220 Verify Operations Yesterday widget is visible."""
        home_page = HomeWebPage(driver)

        assert home_page.text_is_visible("Operations Yesterday"), (
            "Operations Yesterday widget title should be visible "
            "on the Home page"
        )

        # Verify the widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Operations Yesterday')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Operations Yesterday widget container should be visible"
        )
