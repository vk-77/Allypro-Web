"""
Customer Details - Service Location Status option tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen
from tests.web.test_01_2_customer_details_information.test_service_location_settings import (
    open_service_location_menu,
)


@pytest.mark.usefixtures("driver")
class TestServiceLocationStatus:
    """
    Verify Service Location Status modal.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_service_location_status.py -v
    """

    def test_c70464_service_location_status_modal_opens(self, driver):
        """C70464 Verify Service Location Status modal opens."""
        open_service_location_menu(driver, "Status")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Status modal should be visible"
        )
        assert page.text_is_visible("Status"), "Modal should display Status title"

    def test_c70465_service_location_status_modal_has_options(self, driver):
        """C70465 Verify Status modal has status selection options."""
        open_service_location_menu(driver, "Status")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        has_select = page.element_exists(By.CSS_SELECTOR, ".modal select")
        has_radio = page.element_exists(By.CSS_SELECTOR, ".modal input[type='radio']")
        has_dropdown = page.element_exists(By.CSS_SELECTOR, ".modal .dropdown")
        assert has_select or has_radio or has_dropdown, (
            "Status modal should have status selection controls"
        )

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
