"""
Home - Account Updates widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage


@pytest.mark.usefixtures("driver")
class TestAccountUpdates:
    """
    Verify Account Updates widget on the Home page.

    Usage:
        pytest tests/web/test_10_home/test_10_account_updates.py -v
    """

    def test_c70234_verify_account_updates_widget_visible(self, driver):
        """C70234 Verify Account Updates widget is visible."""
        home_page = HomeWebPage(driver)

        assert home_page.text_is_visible("Account Updates"), (
            "Account Updates widget title should be visible on the Home page"
        )

        # Verify the widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Account Updates')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Account Updates widget container should be visible"
        )
