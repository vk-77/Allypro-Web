"""
Customer Details - Nearby Services tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestNearbyServices:
    """
    Verify Nearby Services modal functionality.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_nearby_services.py -v
    """

    def test_c70513_nearby_services_button_visible(self, driver):
        """C70513 Verify Nearby Services button is visible."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Nearby Services") or page.element_is_visible(
            By.CSS_SELECTOR,
            "[onclick*='NearbyService'], [data-action='nearby-services'], "
            "button[id*='NearbyService']"
        ), "Nearby Services button should be visible"

    def test_c70514_nearby_services_modal_opens(self, driver):
        """C70514 Verify Nearby Services modal opens when clicked."""
        page = BaseWebPage(driver)
        page.find_by_text("Nearby Services").click()
        wait_for_loading_screen(driver)

        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Nearby Services modal should be visible"
        )

    def test_c70515_nearby_services_modal_has_map(self, driver):
        """C70515 Verify Nearby Services modal contains a map or list."""
        page = BaseWebPage(driver)
        page.find_by_text("Nearby Services").click()
        wait_for_loading_screen(driver)

        assert page.element_is_visible(By.CSS_SELECTOR, ".modal .modal-body"), (
            "Modal body should be visible with nearby services content"
        )

    def test_c70516_nearby_services_modal_close(self, driver):
        """C70516 Verify Nearby Services modal can be closed."""
        page = BaseWebPage(driver)
        page.find_by_text("Nearby Services").click()
        wait_for_loading_screen(driver)

        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "Nearby Services modal should be closed"
        )
