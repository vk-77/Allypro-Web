"""
Customer Details - Customer Settings widget tests.

Validates the Customer Settings widget fields and dropdown menu options
displayed on the Information tab.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestCustomerSettings:
    """
    Verify Customer Settings widget fields and menu options on the
    Information tab.

    Usage:
        pytest tests/web/customer_information/test_customer_settings.py -v
    """

    def test_c70412_customer_settings_widget_visible(self, driver):
        """C70412 Verify Customer Settings widget is visible."""
        page = BasePage(driver)
        assert page.text_is_visible("Customer Settings"), (
            "Customer Settings widget should be visible"
        )

    def test_c70413_customer_settings_displays_customer_name(self, driver):
        """C70413 Verify Customer Settings displays customer name field."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .customerName, "
            "#content .customer-setting #spnSettingCustomerName"
        ), "Customer name should be displayed in Customer Settings"

    def test_c70414_customer_settings_displays_address(self, driver):
        """C70414 Verify Customer Settings displays address."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .address, "
            "#content .customer-setting #spnSettingAddress"
        ), "Address should be displayed in Customer Settings"

    def test_c70415_customer_settings_displays_city_state_zip(self, driver):
        """C70415 Verify Customer Settings displays city, state, zip."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .cityStateZip, "
            "#content .customer-setting #spnSettingCityStateZip"
        ), "City/State/Zip should be displayed in Customer Settings"

    def test_c70416_customer_settings_displays_phone(self, driver):
        """C70416 Verify Customer Settings displays phone number."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .phone, "
            "#content .customer-setting [id*='Phone']"
        ), "Phone number should be displayed in Customer Settings"

    def test_c70417_customer_settings_displays_email(self, driver):
        """C70417 Verify Customer Settings displays email."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .email, "
            "#content .customer-setting [id*='Email']"
        ), "Email should be displayed in Customer Settings"

    def test_c70418_customer_settings_displays_type(self, driver):
        """C70418 Verify Customer Settings displays customer type."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .type, "
            "#content .customer-setting [id*='Type']"
        ), "Customer type should be displayed"

    def test_c70419_customer_settings_displays_status(self, driver):
        """C70419 Verify Customer Settings displays status."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .status, "
            "#content .customer-setting [id*='Status']"
        ), "Status should be displayed"

    def test_c70420_customer_settings_displays_billing_cycle(self, driver):
        """C70420 Verify Customer Settings displays billing cycle."""
        page = BasePage(driver)
        assert page.text_is_visible("Billing Cycle") or page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting [id*='BillingCycle']"
        ), "Billing cycle should be displayed"

    def test_c70421_customer_settings_displays_payment_terms(self, driver):
        """C70421 Verify Customer Settings displays payment terms."""
        page = BasePage(driver)
        assert page.text_is_visible("Payment Terms") or page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting [id*='PaymentTerm']"
        ), "Payment terms should be displayed"

    def test_c70422_customer_settings_displays_rate_template(self, driver):
        """C70422 Verify Customer Settings displays rate template."""
        page = BasePage(driver)
        assert page.text_is_visible("Rate Template") or page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting [id*='RateTemplate']"
        ), "Rate template should be displayed"

    def test_c70423_customer_settings_displays_tax_code(self, driver):
        """C70423 Verify Customer Settings displays tax code."""
        page = BasePage(driver)
        assert page.text_is_visible("Tax Code") or page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting [id*='TaxCode']"
        ), "Tax code should be displayed"

    def test_c70424_customer_settings_dropdown_is_clickable(self, driver):
        """C70424 Verify Customer Settings dropdown menu is clickable."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .dropdownOuter-Options"
        ), "Dropdown options should be visible after click"

    def test_c70425_dropdown_has_settings_option(self, driver):
        """C70425 Verify dropdown contains 'Settings' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("Settings"), "'Settings' option should be in dropdown"

    def test_c70426_dropdown_has_status_option(self, driver):
        """C70426 Verify dropdown contains 'Status' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("Status"), "'Status' option should be in dropdown"

    def test_c70427_dropdown_has_update_address_option(self, driver):
        """C70427 Verify dropdown contains 'Update Address' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("Update Address"), (
            "'Update Address' option should be in dropdown"
        )

    def test_c70428_dropdown_has_view_address_history_option(self, driver):
        """C70428 Verify dropdown contains 'View Address History' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("View Address History"), (
            "'View Address History' option should be in dropdown"
        )

    def test_c70429_dropdown_has_custom_fields_option(self, driver):
        """C70429 Verify dropdown contains 'Custom Fields' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("Custom Fields"), (
            "'Custom Fields' option should be in dropdown"
        )

    def test_c70430_dropdown_has_customer_portal_option(self, driver):
        """C70430 Verify dropdown contains 'Customer Portal' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("Customer Portal"), (
            "'Customer Portal' option should be in dropdown"
        )

    def test_c70431_dropdown_has_payment_accounts_option(self, driver):
        """C70431 Verify dropdown contains 'Payment Accounts' option."""
        customer_page = CustomerPage(driver)
        customer_page.open_customer_settings_menu()
        page = BasePage(driver)
        assert page.text_is_visible("Payment Accounts"), (
            "'Payment Accounts' option should be in dropdown"
        )

    def test_c70432_customer_settings_widget_card_header(self, driver):
        """C70432 Verify Customer Settings card header text."""
        page = BasePage(driver)
        header = page.find_visible(
            By.CSS_SELECTOR,
            "#content .customer-setting .cardHeader-Wrap"
        )
        assert header is not None, "Customer Settings card header should be visible"

    def test_c70433_customer_settings_widget_layout(self, driver):
        """C70433 Verify Customer Settings widget has correct layout structure."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#content .customer-setting"
        ), "Customer Settings widget container should be visible"
