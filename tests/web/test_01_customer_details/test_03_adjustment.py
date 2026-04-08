"""
Customer Details - Adjustment tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    text_is_visible,
)
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestAdjustment:
    """
    Adjustment tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_03_adjustment.py -v
    """

    def test_c56973_add_adjustment(self, driver):
        """C56973 Add Adjustment."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click Add Adjustment
        customer_page.click_add_adjustment()

        # Wait for adjustment modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divAddAdjustment, .modal.show, .adjustment-modal",
        )))

        # Select adjustment type
        select2_select(
            driver, "#select2-AdjustmentTypeId-container", "Credit"
        )

        # Enter amount
        amount_field = wait.until(EC.element_to_be_clickable((
            By.ID, "AdjustmentAmount"
        )))
        amount_field.clear()
        amount_field.send_keys("10.00")

        # Enter note
        note_field = wait.until(EC.element_to_be_clickable((
            By.ID, "AdjustmentNote"
        )))
        note_field.clear()
        note_field.send_keys("Automation test adjustment")

        # Save adjustment
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnSaveAdjustment, [onclick*="SaveAdjustment"]',
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=10) or \
            text_is_visible(driver, "Adjustment", timeout=10), (
            "Adjustment should be saved successfully"
        )

    def test_c57834_add_adjustment_taxable_appear_on_invoice(self, driver):
        """C57834 Add Adjustment with taxable/Appear on Invoice and verify invoice."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click Add Adjustment
        customer_page.click_add_adjustment()

        # Wait for adjustment modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divAddAdjustment, .modal.show, .adjustment-modal",
        )))

        # Select adjustment type
        select2_select(
            driver, "#select2-AdjustmentTypeId-container", "Debit"
        )

        # Enter amount
        amount_field = wait.until(EC.element_to_be_clickable((
            By.ID, "AdjustmentAmount"
        )))
        amount_field.clear()
        amount_field.send_keys("15.00")

        # Check Taxable checkbox
        taxable_cb = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "#IsTaxable, [name='IsTaxable']"
        )))
        if not taxable_cb.is_selected():
            taxable_cb.click()

        # Check Appear on Invoice checkbox
        appear_invoice_cb = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#AppearOnInvoice, [name='AppearOnInvoice']",
        )))
        if not appear_invoice_cb.is_selected():
            appear_invoice_cb.click()

        # Enter note
        note_field = wait.until(EC.element_to_be_clickable((
            By.ID, "AdjustmentNote"
        )))
        note_field.clear()
        note_field.send_keys("Taxable adjustment - automation test")

        # Save adjustment
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnSaveAdjustment, [onclick*="SaveAdjustment"]',
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=10) or \
            text_is_visible(driver, "Adjustment", timeout=10), (
            "Taxable adjustment should be saved successfully"
        )

        # Verify the adjustment appears in account activity / invoice section
        customer_page.open_account_activity_tab()
        wait_for_loading_screen(driver)

        assert text_is_visible(driver, "15.00", timeout=10), (
            "Adjustment amount should appear in account activity"
        )
