"""
Customer Details - Audit tests.

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
class TestAudit:
    """
    Audit tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_14_audit.py -v
    """

    def test_c56992_audit_load_is_working(self, driver):
        """C56992 Audit Load is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Audit tab
        customer_page.open_audit_tab()
        wait_for_loading_screen(driver)

        # Verify audit tab content is loaded
        assert text_is_visible(driver, "Audit", timeout=10) or \
            text_is_visible(driver, "Change", timeout=10) or \
            text_is_visible(driver, "History", timeout=10), (
            "Audit tab content should be displayed"
        )

        # Verify audit grid/table is present
        audit_table = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "#parentTabContainer_6 table, "
            "#parentTabContainer_6 .grid, "
            "#parentTabContainer_6 .k-grid, "
            ".audit-grid",
        )))
        assert audit_table is not None, (
            "Audit grid should be present"
        )
