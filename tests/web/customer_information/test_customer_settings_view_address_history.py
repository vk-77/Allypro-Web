"""
Customer Details - Customer Settings View Address History option tests.

Validates that the View Address History modal opens from the Customer
Settings dropdown and displays a data grid with historical records.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsViewAddressHistory:
    """
    Verify View Address History modal from Customer Settings dropdown.

    Usage:
        pytest tests/web/customer_information/test_customer_settings_view_address_history.py -v
    """

    def test_c70454_address_history_modal_opens(self, driver):
        """C70454 Verify Address History modal opens from dropdown."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("View Address History")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Address History modal should be visible"
        )

    def test_c70455_address_history_modal_has_grid(self, driver):
        """C70455 Verify Address History modal contains a data grid."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("View Address History")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".modal table, .modal .k-grid, .modal .grid"
        ), "Address History modal should contain a grid/table"

    def test_c70456_address_history_modal_close(self, driver):
        """C70456 Verify Address History modal can be closed."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("View Address History")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        page.element_is_visible(By.CSS_SELECTOR, ".modal")

        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "Address History modal should be closed"
        )
