"""
Customer Details - View Services tests.

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
class TestViewServices:
    """
    View Services tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_06_view_services.py -v
    """

    def test_c56979_view_services(self, driver):
        """C56979 View Services."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click View Services
        customer_page.click_view_services()

        # Wait for services modal/section to appear
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divAllServices, .modal.show, .services-modal, "
            "#divCustomerAllServices",
        )))
        wait_for_loading_screen(driver)

        # Verify services are displayed
        assert text_is_visible(driver, "Service", timeout=10), (
            "Services list should be displayed"
        )

        # Verify at least one service row exists
        service_rows = driver.find_elements(
            By.CSS_SELECTOR,
            "#divAllServices tbody tr, #divCustomerAllServices tbody tr, "
            ".services-grid tbody tr",
        )
        assert len(service_rows) > 0, (
            "At least one service should be displayed"
        )
