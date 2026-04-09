"""
Customer Details - service activity tests.

Validates that the Service Activity tab loads and displays the
activity grid on the Customer Details page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, text_is_visible
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestServiceActivity:
    """
    Service Activity tests for Customer Details.

    Usage:
        pytest tests/web/customer/test_service_activity.py -v
    """

    def test_c56985_view_service_activities(self, driver):
        """C56985 View Service Activities."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Service Activity tab
        customer_page.open_service_activity_tab()

        # Wait for service activity pane to be active
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#parentTabContainer_3.tab-pane.active",
        )))
        wait_for_loading_screen(driver)

        # Verify service activity content is displayed
        assert text_is_visible(driver, "Service", timeout=10) or \
            text_is_visible(driver, "Activity", timeout=10), (
            "Service Activity tab content should be displayed"
        )

        # Verify the grid/table has loaded
        activity_table = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "#parentTabContainer_3 table, "
            "#parentTabContainer_3 .grid, "
            "#parentTabContainer_3 .k-grid",
        )))
        assert activity_table is not None, (
            "Service activity grid should be present"
        )
