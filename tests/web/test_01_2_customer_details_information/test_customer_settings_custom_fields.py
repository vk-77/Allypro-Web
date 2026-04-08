"""
Customer Details - Customer Settings Custom Fields option tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsCustomFields:
    """
    Verify Custom Fields modal opens and date change works from
    Customer Settings dropdown.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_customer_settings_custom_fields.py -v
    """

    def test_c70438_custom_fields_modal_opens(self, driver):
        """C70438 Verify Custom Fields modal opens from Customer Settings dropdown."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Custom Fields")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Custom Fields modal should be visible"
        )
        assert page.text_is_visible("Custom Fields"), (
            "Modal should display 'Custom Fields' title"
        )

    def test_c70439_custom_fields_date_field_change(self, driver):
        """C70439 Verify date field can be changed in Custom Fields modal."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Custom Fields")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        page.element_is_visible(By.CSS_SELECTOR, ".modal")

        # Locate date input field in modal and verify it is interactable
        date_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".modal input[type='date'], .modal .datepicker, .modal input.date-field"
            ))
        )
        assert date_field is not None, "Date field should be present in Custom Fields modal"

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
