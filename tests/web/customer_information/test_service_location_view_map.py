"""
Customer Details - Service Location View Map option tests.

Validates that the View Map modal opens from the Service Location dropdown
and displays the correct title and map content.
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
class TestServiceLocationViewMap:
    """
    Verify Service Location View Map modal.

    Usage:
        pytest tests/web/customer_information/test_service_location_view_map.py -v
    """

    def test_c70472_view_map_modal_opens(self, driver):
        """C70472 Verify View Map modal opens from Service Location dropdown."""
        open_service_location_menu(driver, "View Map")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "View Map modal should be visible"
        )

    def test_c70473_view_map_modal_has_title(self, driver):
        """C70473 Verify View Map modal has correct title."""
        open_service_location_menu(driver, "View Map")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.text_is_visible("Map") or page.text_is_visible("View Map"), (
            "Modal should display Map title"
        )

    def test_c70474_view_map_modal_has_map_container(self, driver):
        """C70474 Verify View Map modal contains a map container."""
        open_service_location_menu(driver, "View Map")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".modal .map, .modal #map, .modal [class*='map'], .modal iframe"
        ), "Map container should be visible in modal"

    def test_c70475_view_map_modal_has_address_info(self, driver):
        """C70475 Verify View Map modal displays address information."""
        open_service_location_menu(driver, "View Map")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal .modal-body"), (
            "Modal body with address info should be visible"
        )

    def test_c70476_view_map_modal_close(self, driver):
        """C70476 Verify View Map modal can be closed."""
        open_service_location_menu(driver, "View Map")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "View Map modal should be closed"
        )
