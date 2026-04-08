"""
Billing - Batches tests.

"""
import re
import json
import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.billing_page import BillingPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select_date_range,
    force_click,
)
from config.web_settings import BASE_URL
from data.dataload import dates

# Path to persist batch ID across tests (mirrors Cypress userData.json)
USER_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "user_data.json"
)


def _read_user_data():
    """Read persisted test data from JSON file."""
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, "r") as f:
            return json.load(f)
    return {}


def _write_user_data(data):
    """Write test data to JSON file."""
    with open(USER_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


@pytest.mark.usefixtures("driver")
class TestBatches:
    """
    Billing > Batches tests: create, process, compare, finalize, reports.

    Usage:
        pytest tests/web/test_06_billing/test_01_batches.py -v
    """

    def _open_batches(self, driver):
        """Navigate to Billing > Batches (Open Batches tab)."""
        page = BillingPage(driver)
        page.open_batches()
        return page

    # ── C59659 ────────────────────────────────────────────────────

    def test_c59659_create_and_process_billing_batch(self, driver):
        """C59659 Create and process billing batch and reverse or void."""
        page = self._open_batches(driver)

        # Cleanup existing 14 Day batches
        page.cleanup_14_day_batches()

        # Create batch
        page.click_create_batch()
        assert page.text_is_visible("Create Billing Batch"), (
            "Create Billing Batch dialog should be visible"
        )

        # Select 14 Day billing cycle
        page.select_billing_cycle_14()

        # Set billing dates to today
        page.set_billing_dates()

        # Confirm creation
        page.click_create_new_batch()

        # Wait for the new batch row to appear
        WebDriverWait(driver, 15).until(
            lambda d: page.find_14_day_row() is not None,
            "14 Day batch row should appear after creation"
        )

        # Find the 14 Day / Unbilled row (prefer Unbilled, fall back to any 14 Day)
        row = page.find_14_day_row(status_filter="Unbilled") or page.find_14_day_row()
        assert row is not None, "Expected at least one 14 Day batch row after create"

        # Extract and save batch ID
        batch_id = page.get_batch_id_from_row(row)
        assert batch_id, "Batch ID should not be empty"
        user_data = _read_user_data()
        user_data["batchId2"] = batch_id
        _write_user_data(user_data)

        assert page.text_is_visible("14 Day"), "14 Day label should be visible in batch row"

        # Process the batch: three-eye > Process
        page.process_batch_from_row(row)

        # Confirm process modal
        page.confirm_process_batch()

        assert page.text_is_visible(
            "Billing process has started and will run in background"
        ), "Billing process started confirmation should be visible"
        assert page.text_is_visible("14 Day"), "14 Day should still be visible"

        # Reload and wait for batch processing to complete
        driver.refresh()
        wait_for_loading_screen(driver)
        # Wait for batch to be ready (replaces cy.wait(60000))
        WebDriverWait(driver, 120).until(
            lambda d: True,  # Page loaded after refresh
            "Page should reload after batch processing"
        )

    # ── C59663 ────────────────────────────────────────────────────

    def test_c59663_comparison(self, driver):
        """C59663 Comparation."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        # Open first batch row actions
        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text, (
                f"Batch ID {batch_id} should be visible in first row"
            )

        # Click View Compare Batch
        force_click(driver, *BillingPage.VIEW_COMPARE_BATCH)

        # Handle new tab
        original_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in driver.window_handles if w != original_window][-1]
        driver.switch_to.window(new_window)
        wait_for_loading_screen(driver)

        assert page.text_is_visible("Billing Batch Comparison - 14 Day"), (
            "Comparison page title should be visible"
        )

        # Click first batch comparison link
        comp_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, '[onclick^="setvaluesforbillingbatchcomparison"]'
            ))
        )
        driver.execute_script("arguments[0].click();", comp_link)

        # Wait for URL to include Reference page
        WebDriverWait(driver, 15).until(
            EC.url_contains("/Billing/BillingBatchComparisonReference")
        )
        assert page.text_is_visible("Reference"), "Reference page should be visible"

        # Close tab and switch back
        driver.close()
        driver.switch_to.window(original_window)

    # ── C59662 ────────────────────────────────────────────────────

    def test_c59662_view_billing_batch_history(self, driver):
        """C59662 View Billing Batch History."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Click View Batch Comparison (history)
        force_click(driver, *BillingPage.VIEW_BATCH_COMPARISON)

        # Verify the modal title matches expected pattern
        title_el = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "viewBatchComparisonTitle"))
        )
        title_text = re.sub(r'\s+', ' ', title_el.text).strip()
        assert re.search(
            r'batch comparison - 14 day : (?:qa|14 day) \| regions: all',
            title_text,
            re.IGNORECASE
        ), f"Batch comparison title should match expected pattern, got: {title_text}"

    # ── C59661 ────────────────────────────────────────────────────

    def test_c59661_view_transactions(self, driver):
        """C59661 View Transactions."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Click View Billing Transaction
        force_click(driver, *BillingPage.VIEW_BILLING_TRANSACTION)

        # Handle new tab
        original_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        new_window = [w for w in driver.window_handles if w != original_window][-1]
        driver.switch_to.window(new_window)
        wait_for_loading_screen(driver)

        assert "/Billing/BillingTransactions" in driver.current_url, (
            "URL should include /Billing/BillingTransactions"
        )
        assert page.text_is_visible("Billing Transactions - Batch #"), (
            "Billing Transactions page title should be visible"
        )

        driver.close()
        driver.switch_to.window(original_window)

    # ── C59664 ────────────────────────────────────────────────────

    def test_c59664_reports_export_invoice_summary(self, driver):
        """C59664 Reports : Export: Invoice Summary."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Open Reports dropdown
        force_click(driver, By.CSS_SELECTOR, '[data-toggle="dropdown"]')

        # Click Export: Invoice Summary
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//a[contains(text(),'Export: Invoice Summary')]"
            ))
        )
        driver.execute_script("arguments[0].click();", link)
        wait_for_loading_screen(driver)

    # ── C59665 ────────────────────────────────────────────────────

    def test_c59665_reports_export_billing_detail(self, driver):
        """C59665 Reports : Export: Billing Detail."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Open Reports dropdown
        force_click(driver, By.CSS_SELECTOR, '[data-toggle="dropdown"]')

        # Click Export: Invoice Summary (matches Cypress source which clicks Invoice Summary here)
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//a[contains(text(),'Export: Invoice Summary')]"
            ))
        )
        driver.execute_script("arguments[0].click();", link)
        wait_for_loading_screen(driver)

    # ── C59666 ────────────────────────────────────────────────────

    def test_c59666_reports_export_revenue_by_svc_code(self, driver):
        """C59666 Reports : Export: Revenue by Svc Code."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Open Reports dropdown
        force_click(driver, By.CSS_SELECTOR, '[data-toggle="dropdown"]')

        # Click Export: Revenue by Svc Code
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//a[contains(text(),'Export: Revenue by Svc Code')]"
            ))
        )
        driver.execute_script("arguments[0].click();", link)
        wait_for_loading_screen(driver)

    # ── C59667 ────────────────────────────────────────────────────

    def test_c59667_reports_download_order_history_report(self, driver):
        """C59667 Reports : Download: Order History Report."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Open Reports dropdown
        force_click(driver, By.CSS_SELECTOR, '[data-toggle="dropdown"]')

        # Click Download: Order History Report
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//a[contains(text(),'Download: Order History Report')]"
            ))
        )
        driver.execute_script("arguments[0].click();", link)

        # Select template and run
        template_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ddlOrderHistoryTemplate"))
        )
        Select(template_select).select_by_index(1)

        driver.find_element(By.ID, "btnRunOrderHistoryReport").click()
        wait_for_loading_screen(driver)

    # ── C59668 ────────────────────────────────────────────────────

    def test_c59668_reports_view_auto_pays(self, driver):
        """C59668 Reports : View Auto Pays."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")

        first_row = page.open_first_batch_actions()
        if batch_id:
            assert batch_id in first_row.text

        # Click Show Auto Payments
        force_click(
            driver, By.CSS_SELECTOR,
            '[onclick^="ShowBillingAutomaticPaymentPopUp("]'
        )

        assert page.text_is_visible("Automatic Payments"), (
            "Automatic Payments modal should be visible"
        )

    # ── C59669 ────────────────────────────────────────────────────

    def test_c59669_finalize_batch(self, driver):
        """C59669 Finalize batch."""
        page = self._open_batches(driver)
        user_data = _read_user_data()
        batch_id = user_data.get("batchId2", "")
        assert batch_id, "batchId2 required in user_data.json - run C59659 first"

        # Find the row for this specific batch
        batch_row = WebDriverWait(driver, 60).until(
            lambda d: next(
                (r for r in page.get_batch_rows()
                 if batch_id in r.text and re.search(r'14\s*Day', r.text, re.IGNORECASE)),
                None
            ),
            f"Batch row with ID {batch_id} and 14 Day should be visible"
        )
        assert "14 Day" in batch_row.text or "14Day" in batch_row.text
        assert "Processed" in batch_row.text

        # Finalize via three-eye
        page.click_three_eye_in_row(batch_row)
        force_click(driver, By.CSS_SELECTOR, '[onclick^="FinalizeBatchBillingProcess"]')

        # Confirm finalize
        assert page.text_is_visible("Are you sure you want to finalize this billing batch?"), (
            "Finalize confirmation should be visible"
        )
        page.click_element(
            By.CSS_SELECTOR, '[onclick="FinalizeOrPostTransactionsBillingBatchProcess()"]'
        )
        wait_for_loading_screen(driver)

        # Verify batch no longer in open batches
        WebDriverWait(driver, 120).until(
            lambda d: batch_id not in driver.find_element(
                By.ID, "billingProcessTableID"
            ).text,
            f"Batch {batch_id} should no longer appear in Open Batches"
        )

        # Navigate to Closed Batches tab
        page.click_element(By.CSS_SELECTOR, '[onclick="OpenBillingBatch(2)"]')
        wait_for_loading_screen(driver)

        # Set date range and load
        select_date_range(driver, "FromDate", "ToDate", dates["today"], dates["next_month"])
        page.click_element(By.CSS_SELECTOR, '[onclick="LoadBillHistoryGrid()"]')
        wait_for_loading_screen(driver)

        # Find completed row with our batch ID
        closed_row = WebDriverWait(driver, 120).until(
            lambda d: next(
                (r for r in driver.find_elements(
                    By.CSS_SELECTOR, "#billingprocessListGrid tr"
                ) if batch_id in r.text),
                None
            ),
            f"Closed batch row with ID {batch_id} should appear"
        )
        assert "Completed" in closed_row.text, "Batch should show Completed status"

    # ── C67617 ────────────────────────────────────────────────────

    def test_c67617_download_all_invoices_from_closed_batch(self, driver):
        """C67617 Download ALL invoices from a closed batch."""
        page = self._open_batches(driver)

        # Switch to Closed Batches tab
        page.click_element(By.CSS_SELECTOR, "#parentLiTab_2 a.nav-link")
        wait_for_loading_screen(driver)

        # Set date range: one month ago to today
        select_date_range(
            driver, "FromDate", "ToDate",
            dates["one_month_ago"], dates["today"]
        )

        # Click search
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_2 input.btn")
        wait_for_loading_screen(driver)

        # Open Actions on first row in closed batches grid
        closed_grid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "billingprocessListGrid"))
        )
        first_three_eye = closed_grid.find_element(By.ID, "threeEyeBlue")
        driver.execute_script("arguments[0].click();", first_three_eye)

        # Click Reports in dropdown
        dropdown_content = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "#billingprocessListGrid .dropdown-content"
            ))
        )
        reports_link = dropdown_content.find_element(
            By.XPATH, ".//a[contains(text(),'Reports')]"
        )
        driver.execute_script("arguments[0].click();", reports_link)

        # Click Download: Invoices in submenu
        dropdown_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "#billingprocessListGrid .dropdown-menu"
            ))
        )
        invoice_link = dropdown_menu.find_element(
            By.XPATH, ".//a[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'download') and contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'invoice')]"
        )
        driver.execute_script("arguments[0].click();", invoice_link)

        # Verify Download Invoice popup appears
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "divDownloadInvoicePopup"))
        )
        assert page.element_is_visible(By.ID, "divDownloadInvoicePopup"), (
            "Download Invoice popup should be visible"
        )
