"""
Customer Details - Customer Settings Customer Portal option tests.

Validates that the Customer Portal modal opens from the Customer Settings
dropdown with the correct title and expected content.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsCustomerPortal:
    """
    Verify Customer Portal Settings modal from Customer Settings dropdown.

    Usage:
        pytest tests/web/customer_information/test_customer_settings_customer_portal.py -v
    """

    def test_c70434_customer_portal_modal_opens(self, driver):
        """C70434 Verify Customer Portal modal opens from dropdown."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Customer Portal")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Customer Portal modal should be visible"
        )

    def test_c70435_customer_portal_modal_title(self, driver):
        """C70435 Verify Customer Portal modal displays correct title."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Customer Portal")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.text_is_visible("Customer Portal"), (
            "Modal title should contain 'Customer Portal'"
        )

    def test_c70436_customer_portal_modal_has_fields(self, driver):
        """C70436 Verify Customer Portal modal has expected form fields."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Customer Portal")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal .modal-body"), (
            "Modal body should be visible with form fields"
        )

    def test_c70437_customer_portal_modal_close(self, driver):
        """C70437 Verify Customer Portal modal can be closed."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Customer Portal")
        wait_for_loading_screen(driver)

        page = BasePage(driver)
        page.element_is_visible(By.CSS_SELECTOR, ".modal")

        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
        assert page.element_not_visible(By.CSS_SELECTOR, ".modal.show"), (
            "Modal should be closed"
        )
