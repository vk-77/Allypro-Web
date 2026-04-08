"""
Customer Details - Customer Settings Dropdown Navigation tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsDropdownNavigation:
    """
    Verify Customer Settings dropdown navigation between options.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_customer_settings_dropdown_navigation.py -v
    """

    def test_c70440_dropdown_navigation_opens_each_option(self, driver):
        """C70440 Verify dropdown navigation opens different settings options correctly."""
        customer_page = CustomerPage(driver)
        page = BaseWebPage(driver)

        # Open Settings option
        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Settings modal should open"
        )

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        wait_for_loading_screen(driver)

        # Open Status option
        customer_page.open_customer_settings_menu("Status")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Status modal should open"
        )

    def test_c70441_dropdown_navigation_returns_to_menu(self, driver):
        """C70441 Verify closing a modal returns to the settings dropdown state."""
        customer_page = CustomerPage(driver)
        page = BaseWebPage(driver)

        customer_page.open_customer_settings_menu("Settings")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Settings modal should be visible"
        )

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        wait_for_loading_screen(driver)

        # Verify dropdown can be opened again
        customer_page.open_customer_settings_menu()
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .dropdownOuter-Options"
        ), "Dropdown menu should be accessible again after closing modal"
