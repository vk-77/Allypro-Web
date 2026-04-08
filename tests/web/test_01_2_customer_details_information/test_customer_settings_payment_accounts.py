"""
Customer Details - Customer Settings Payment Accounts option tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettingsPaymentAccounts:
    """
    Verify Payment Accounts modal from Customer Settings dropdown.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_customer_settings_payment_accounts.py -v
    """

    def test_c70442_payment_accounts_modal_opens(self, driver):
        """C70442 Verify Payment Accounts modal opens from dropdown."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Payment Accounts")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Payment Accounts modal should be visible"
        )
        assert page.text_is_visible("Payment Accounts") or page.text_is_visible("Payment"), (
            "Modal should display Payment Accounts title"
        )

    def test_c70443_payment_accounts_modal_content(self, driver):
        """C70443 Verify Payment Accounts modal has expected content."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu("Payment Accounts")
        wait_for_loading_screen(driver)

        page = BaseWebPage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, ".modal .modal-body"), (
            "Modal body should be visible"
        )

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
