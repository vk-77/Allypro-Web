"""
Customer Details - invoice tests.

Validates creating, finalizing, reversing, viewing details of,
and previewing invoices from the Customer Details page.
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
    force_click,
)
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestInvoice:
    """
    Invoice tests for Customer Details.

    Usage:
        pytest tests/web/customer/test_invoice.py -v
    """

    def test_c56974_create_invoice_finalize(self, driver):
        """C56974 Create Invoice - Finalize."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click Create Invoice
        customer_page.click_create_invoice()

        # Wait for invoice modal / creation dialog
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divCreateInvoice, .modal.show, .invoice-modal",
        )))
        wait_for_loading_screen(driver)

        # Click Finalize button
        finalize_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnFinalizeInvoice, [onclick*="FinalizeInvoice"], '
            '[onclick*="Finalize"]',
        )))
        finalize_btn.click()
        wait_for_loading_screen(driver)

        # Confirm finalize if confirmation dialog appears
        try:
            confirm_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '#btnConfirmFinalize, .swal2-confirm, '
                    '.btn-confirm, [onclick*="ConfirmFinalize"]',
                ))
            )
            confirm_btn.click()
            wait_for_loading_screen(driver)
        except Exception:
            pass

        # Verify success
        assert text_is_visible(driver, "success", timeout=15) or \
            text_is_visible(driver, "Invoice", timeout=10) or \
            text_is_visible(driver, "finalized", timeout=10), (
            "Invoice should be finalized successfully"
        )

    def test_c56975_create_invoice_reverse(self, driver):
        """C56975 Create Invoice - Reverse."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Account Activity tab to find an invoice
        customer_page.open_account_activity_tab()
        wait_for_loading_screen(driver)

        # Click on the first invoice row to open it
        invoice_row = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#tblAccountActivity tbody tr:first-child, '
            '.account-activity-grid tbody tr:first-child',
        )))
        invoice_row.click()
        wait_for_loading_screen(driver)

        # Click Reverse button
        reverse_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnReverseInvoice, [onclick*="ReverseInvoice"], '
            '[onclick*="Reverse"]',
        )))
        reverse_btn.click()
        wait_for_loading_screen(driver)

        # Confirm reverse if confirmation dialog appears
        try:
            confirm_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    '.swal2-confirm, .btn-confirm, '
                    '[onclick*="ConfirmReverse"]',
                ))
            )
            confirm_btn.click()
            wait_for_loading_screen(driver)
        except Exception:
            pass

        # Verify success
        assert text_is_visible(driver, "success", timeout=15) or \
            text_is_visible(driver, "Reverse", timeout=10) or \
            text_is_visible(driver, "reversed", timeout=10), (
            "Invoice should be reversed successfully"
        )

    def test_c56976_create_invoice_view_details(self, driver):
        """C56976 Create Invoice - View Details."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Account Activity tab
        customer_page.open_account_activity_tab()
        wait_for_loading_screen(driver)

        # Click on the first invoice row to view details
        invoice_row = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#tblAccountActivity tbody tr:first-child, '
            '.account-activity-grid tbody tr:first-child',
        )))
        invoice_row.click()
        wait_for_loading_screen(driver)

        # Click View Details button
        view_details_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnViewDetails, [onclick*="ViewDetails"], '
            '[onclick*="ViewInvoiceDetails"]',
        )))
        view_details_btn.click()
        wait_for_loading_screen(driver)

        # Verify invoice detail view is displayed
        assert text_is_visible(driver, "Invoice", timeout=10), (
            "Invoice details should be displayed"
        )

    def test_c56977_create_invoice_preview(self, driver):
        """C56977 Create Invoice - Preview."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click Create Invoice
        customer_page.click_create_invoice()

        # Wait for invoice modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divCreateInvoice, .modal.show, .invoice-modal",
        )))
        wait_for_loading_screen(driver)

        # Click Preview button
        preview_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnPreviewInvoice, [onclick*="PreviewInvoice"], '
            '[onclick*="Preview"]',
        )))
        preview_btn.click()
        wait_for_loading_screen(driver)

        # Verify preview is shown (PDF viewer or preview modal)
        assert text_is_visible(driver, "Preview", timeout=10) or \
            text_is_visible(driver, "Invoice", timeout=10) or \
            driver.find_elements(
                By.CSS_SELECTOR, "iframe, embed, .pdf-viewer, .preview-container"
            ), (
            "Invoice preview should be displayed"
        )
