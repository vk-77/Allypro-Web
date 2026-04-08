"""
Customer Details - Service Location Update Address option tests.

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
class TestServiceLocationUpdateAddress:
    """
    Verify Service Location Update Address modal.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_service_location_update_address.py -v
    """

    def test_c70467_update_address_modal_opens(self, driver):
        """C70467 Verify Update Address modal opens from Service Location dropdown."""
        open_service_location_menu(driver, "Update Address")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Update Address modal should be visible"
        )

    def test_c70468_update_address_modal_has_form_fields(self, driver):
        """C70468 Verify Update Address modal has address form fields."""
        open_service_location_menu(driver, "Update Address")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        fields = driver.find_elements(By.CSS_SELECTOR, ".modal input")
        assert len(fields) > 0, "Update Address modal should contain input fields"

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
