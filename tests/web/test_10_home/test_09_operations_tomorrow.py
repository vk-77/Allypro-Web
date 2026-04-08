"""
Home - Operations Tomorrow widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage


@pytest.mark.usefixtures("driver")
class TestOperationsTomorrow:
    """
    Verify Operations Tomorrow widget on the Home page.

    Usage:
        pytest tests/web/test_10_home/test_09_operations_tomorrow.py -v
    """

    def test_c70227_verify_operations_tomorrow_widget_visible(self, driver):
        """C70227 Verify Operations Tomorrow widget is visible."""
        home_page = HomeWebPage(driver)

        assert home_page.text_is_visible("Operations Tomorrow"), (
            "Operations Tomorrow widget title should be visible "
            "on the Home page"
        )

        # Verify the widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Operations Tomorrow')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Operations Tomorrow widget container should be visible"
        )
