"""
Home - Customer Growth widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage


@pytest.mark.usefixtures("driver")
class TestCustomerGrowth:
    """
    Verify Customer Growth chart/widget on the Home page.

    Usage:
        pytest tests/web/test_10_home/test_06_customer_growth.py -v
    """

    def test_c70210_verify_customer_growth_widget_visible(self, driver):
        """C70210 Verify Customer Growth chart/widget is visible."""
        home_page = HomeWebPage(driver)

        assert home_page.text_is_visible("Customer Growth"), (
            "Customer Growth widget title should be visible on the Home page"
        )

        # Verify the chart/widget container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Customer Growth')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Customer Growth widget container should be visible"
        )
