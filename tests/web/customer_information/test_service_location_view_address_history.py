"""
Customer Details - Service Location View Address History tests.

Validates that the View Address History modal opens from the Service
Location dropdown and displays a data grid with historical records.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen
from tests.web.customer_information.test_service_location_settings import (
    open_service_location_menu,
)


@pytest.mark.usefixtures("driver")
class TestServiceLocationViewAddressHistory:
    """
    Verify Service Location View Address History modal.

    Usage:
        pytest tests/web/customer_information/test_service_location_view_address_history.py -v
    """

    def test_c70469_view_address_history_modal_opens(self, driver):
        """C70469 Verify View Address History modal opens."""
        open_service_location_menu(driver, "View Address History")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "View Address History modal should be visible"
        )

    def test_c70470_view_address_history_has_grid(self, driver):
        """C70470 Verify Address History modal has a data grid."""
        open_service_location_menu(driver, "View Address History")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, ".modal table, .modal .k-grid, .modal .grid"
        ), "Address History modal should contain a grid/table"

    def test_c70471_view_address_history_modal_close(self, driver):
        """C70471 Verify Address History modal can be closed."""
        open_service_location_menu(driver, "View Address History")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "Address History modal should be closed"
        )
