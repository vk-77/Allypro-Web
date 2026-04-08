"""
Customer Details - Customer Settings Status option tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsStatus:
    """
    Verify Customer Status modal from Customer Settings dropdown.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_customer_settings_status.py -v
    """

    def test_c70450_status_modal_opens(self, driver):
        """C70450 Verify Status modal opens from Customer Settings dropdown."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Status")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Status modal should be visible"
        )
        assert page.text_is_visible("Status"), (
            "Modal should display Status title"
        )

    def test_c70451_status_modal_has_status_options(self, driver):
        """C70451 Verify Status modal has status selection options."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Status")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal .modal-body"), (
            "Modal body should be visible with status options"
        )

        # Verify there is a status dropdown or radio buttons
        has_select = page.element_exists(By.CSS_SELECTOR, ".modal select")
        has_radio = page.element_exists(By.CSS_SELECTOR, ".modal input[type='radio']")
        has_dropdown = page.element_exists(By.CSS_SELECTOR, ".modal .dropdown")
        assert has_select or has_radio or has_dropdown, (
            "Status modal should contain a status selection control"
        )

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
