"""
Customer Details - Information tab tests.

Validates that the Information tab loads with all expected sections, headers,
balance cards, dropdowns, sub-tabs, and widgets.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestInformation:
    """
    Verify the Customer Details Information tab loads correctly with all
    expected sections, headers, balance cards, dropdowns, tabs, and widgets.

    Usage:
        pytest tests/web/customer_information/test_information.py -v
    """

    def test_c70338_customer_details_page_loads(self, driver):
        """C70338 Verify Customer Details page loads successfully."""
        assert "/CustomerDetails" in driver.current_url, (
            "URL should contain '/CustomerDetails'"
        )

    def test_c70339_customer_name_header_is_visible(self, driver):
        """C70339 Verify customer name header is visible."""
        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, "#spnCustomerName, .customerName"), (
            "Customer name header should be visible"
        )

    def test_c70340_customer_id_is_displayed(self, driver):
        """C70340 Verify customer ID is displayed."""
        page = BasePage(driver)
        assert page.element_is_visible(By.CSS_SELECTOR, "#spnCustomerID, .customerId"), (
            "Customer ID should be visible"
        )

    def test_c70341_balance_cards_are_visible(self, driver):
        """C70341 Verify balance cards section is visible."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, ".balance-card, .balanceCard, #divBalanceCards"
        ), "Balance cards section should be visible"

    def test_c70342_current_balance_card_displayed(self, driver):
        """C70342 Verify Current Balance card is displayed."""
        page = BasePage(driver)
        assert page.text_is_visible("Current Balance"), (
            "Current Balance card should be visible"
        )

    def test_c70343_credit_balance_card_displayed(self, driver):
        """C70343 Verify Credit Balance card is displayed."""
        page = BasePage(driver)
        assert page.text_is_visible("Credit Balance") or page.text_is_visible("Credit"), (
            "Credit Balance card should be visible"
        )

    def test_c70344_service_location_dropdown_visible(self, driver):
        """C70344 Verify service location dropdown is visible."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#ddlServiceLocation, select[name='serviceLocation'], .service-location-dropdown"
        ), "Service location dropdown should be visible"

    def test_c70345_information_tab_is_active(self, driver):
        """C70345 Verify Information tab is the active/default tab."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".tab-pane.active, #parentTabContainer_1.active"
        ), "Information tab should be active by default"

    def test_c70346_contacts_tab_exists(self, driver):
        """C70346 Verify Contacts tab is present."""
        page = BasePage(driver)
        assert page.text_is_visible("Contacts"), "Contacts tab should be visible"

    def test_c70347_service_activity_tab_exists(self, driver):
        """C70347 Verify Service Activity tab is present."""
        page = BasePage(driver)
        assert page.text_is_visible("Service Activity"), (
            "Service Activity tab should be visible"
        )

    def test_c70348_account_activity_tab_exists(self, driver):
        """C70348 Verify Account Activity tab is present."""
        page = BasePage(driver)
        assert page.text_is_visible("Account Activity"), (
            "Account Activity tab should be visible"
        )

    def test_c70487_snapshot_widget_is_visible(self, driver):
        """C70487 Verify Snapshot widget is visible on Information tab."""
        page = BasePage(driver)
        assert page.text_is_visible("Snapshot") or page.element_is_visible(
            By.CSS_SELECTOR, ".snapshot-widget, #divSnapshot"
        ), "Snapshot widget should be visible"

    def test_c70507_services_widget_is_visible(self, driver):
        """C70507 Verify Services widget is visible on Information tab."""
        page = BasePage(driver)
        assert page.text_is_visible("Services") or page.element_is_visible(
            By.CSS_SELECTOR, ".services-widget, #divServices"
        ), "Services widget should be visible"
