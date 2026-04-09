"""
Customer Details - Service Map tests.

Validates the Service Map button visibility and that clicking it opens
the map view on the Customer Details page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestServiceMap:
    """
    Verify Service Map functionality on Customer Details page.

    Usage:
        pytest tests/web/customer_information/test_service_map.py -v
    """

    def test_c70517_service_map_button_visible(self, driver):
        """C70517 Verify Service Map button/link is visible."""
        page = BasePage(driver)
        assert page.text_is_visible("Service Map") or page.element_is_visible(
            By.CSS_SELECTOR,
            "[onclick*='ServiceMap'], [data-action='service-map'], "
            "button[id*='ServiceMap']"
        ), "Service Map button should be visible"

    def test_c70518_service_map_opens(self, driver):
        """C70518 Verify Service Map opens when clicked."""
        page = BasePage(driver)
        page.find_by_text("Service Map").click()
        wait_for_loading_screen(driver)

        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".modal, .map-container, #map, [class*='map']"
        ), "Service Map should be displayed"

    def test_c70519_service_map_has_map_content(self, driver):
        """C70519 Verify Service Map displays map content."""
        page = BasePage(driver)
        page.find_by_text("Service Map").click()
        wait_for_loading_screen(driver)

        # Look for map rendering elements
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".modal .modal-body, .map-container, #map, iframe"
        ), "Map content should be rendered"

        # Close if in modal
        if page.element_exists(By.CSS_SELECTOR, ".modal.show"):
            page.click_element(
                By.CSS_SELECTOR,
                ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
            )
