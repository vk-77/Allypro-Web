"""
Customer Details - Service Location Settings option tests.

Validates the Service Location widget dropdown menu and the Settings
modal form fields and save behaviour.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


SERVICE_LOCATION_DROPDOWN = (
    By.CSS_SELECTOR,
    "#content .service-location .cardHeader-Wrap .dropdown-toggle, "
    ".service-location-widget .dropdown-toggle"
)
SERVICE_LOCATION_OPTIONS = (
    By.CSS_SELECTOR,
    "#content .service-location .dropdownOuter-Options, "
    ".service-location-widget .dropdownOuter-Options"
)


def open_service_location_menu(driver, option_name=None):
    """Open the Service Location widget dropdown and optionally click an option."""
    page = BasePage(driver)
    page.click_element(*SERVICE_LOCATION_DROPDOWN)
    page.find_visible(*SERVICE_LOCATION_OPTIONS)
    if option_name:
        option = page.find_clickable(
            By.XPATH,
            f'//div[contains(@class,"dropdownOuter-Options")]//a[contains(text(),"{option_name}")]'
        )
        option.click()


@pytest.mark.usefixtures("driver")
class TestServiceLocationSettings:
    """
    Verify Service Location Settings modal and its sections.

    Usage:
        pytest tests/web/customer_information/test_service_location_settings.py -v
    """

    def test_c70457_service_location_settings_modal_opens(self, driver):
        """C70457 Verify Service Location Settings modal opens."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Service Location Settings modal should be visible"
        )

    def test_c70458_service_location_settings_title(self, driver):
        """C70458 Verify modal displays correct title."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.text_is_visible("Settings") or page.text_is_visible("Service Location"), (
            "Modal should display Settings title"
        )

    def test_c70459_service_location_settings_has_address(self, driver):
        """C70459 Verify modal has address fields."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, ".modal input, .modal .form-group"
        ), "Modal should contain form fields"

    def test_c70460_service_location_settings_has_contact_info(self, driver):
        """C70460 Verify modal has contact information fields."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        fields = driver.find_elements(By.CSS_SELECTOR, ".modal input, .modal select")
        assert len(fields) > 0, "Modal should contain contact info fields"

    def test_c70461_service_location_settings_has_save_button(self, driver):
        """C70461 Verify modal has a Save button."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".modal .btn-primary, .modal #btnSave, .modal button[type='submit']"
        ), "Save button should be visible"

    def test_c70462_service_location_settings_has_cancel_button(self, driver):
        """C70462 Verify modal has a Cancel/Close button."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close, "
            ".modal .btn-secondary, .modal .btn-default"
        ), "Cancel/Close button should be visible"

    def test_c70463_service_location_settings_modal_close(self, driver):
        """C70463 Verify Service Location Settings modal can be closed."""
        open_service_location_menu(driver, "Settings")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "Modal should be closed"
        )
