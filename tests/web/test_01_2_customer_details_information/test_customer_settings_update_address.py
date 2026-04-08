"""
Customer Details - Customer Settings Update Address option tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsUpdateAddress:
    """
    Verify Update Address modal, update the address and rollback.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_customer_settings_update_address.py -v
    """

    def test_c70453_update_address_and_rollback(self, driver):
        """C70453 Verify address can be updated and rolled back."""
        customer_page = CustomerPage(driver)
        page = BaseWebPage(driver)

        # Capture original address
        original_address = page.get_text(
            By.CSS_SELECTOR,
            "#content .customer-setting .address, "
            "#content .customer-setting #spnSettingAddress"
        )

        # Open Update Address modal
        customer_page.open_customer_settings_menu("Update Address")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Update Address modal should be visible"
        )

        # Find address field and modify it
        address_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".modal #txtAddress, .modal input[name='address'], .modal #Address"
            ))
        )
        test_address = "123 Test St"
        address_field.clear()
        address_field.send_keys(test_address)

        # Save changes
        save_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".modal .btn-primary, .modal #btnSave, .modal button[type='submit']"
            ))
        )
        save_btn.click()
        wait_for_loading_screen(driver)

        # Rollback: reopen Update Address and restore original
        customer_page.open_customer_settings_menu("Update Address")
        wait_for_loading_screen(driver)

        address_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".modal #txtAddress, .modal input[name='address'], .modal #Address"
            ))
        )
        address_field.clear()
        address_field.send_keys(original_address)

        save_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                ".modal .btn-primary, .modal #btnSave, .modal button[type='submit']"
            ))
        )
        save_btn.click()
        wait_for_loading_screen(driver)
