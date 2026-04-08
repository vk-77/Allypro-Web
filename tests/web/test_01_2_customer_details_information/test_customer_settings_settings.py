"""
Customer Details - Customer Settings Settings option tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsSettings:
    """
    Verify Settings modal sections and form fields from Customer Settings dropdown.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_customer_settings_settings.py -v
    """

    def test_c70444_settings_modal_opens(self, driver):
        """C70444 Verify Settings modal opens from Customer Settings dropdown."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Settings modal should be visible"
        )

    def test_c70445_settings_modal_has_general_section(self, driver):
        """C70445 Verify Settings modal has General section."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.text_is_visible("General"), (
            "General section should be visible in Settings modal"
        )

    def test_c70446_settings_modal_has_billing_section(self, driver):
        """C70446 Verify Settings modal has Billing section."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.text_is_visible("Billing"), (
            "Billing section should be visible in Settings modal"
        )

    def test_c70447_settings_modal_has_form_fields(self, driver):
        """C70447 Verify Settings modal has form input fields."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        fields = driver.find_elements(
            By.CSS_SELECTOR, ".modal input, .modal select, .modal textarea"
        )
        assert len(fields) > 0, "Settings modal should contain form fields"

    def test_c70448_settings_modal_close(self, driver):
        """C70448 Verify Settings modal can be closed without saving."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        page.element_is_visible(By.CSS_SELECTOR, ".modal")

        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "Settings modal should be closed"
        )
