"""
Page object for the Elements Billing pages (Batches, Pre-Billing, General Ledger).
"""
import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .base_web_page import BaseWebPage
from config.web_settings import DEFAULT_WAIT


class BillingPage(BaseWebPage):
    """
    Page object for Billing section pages.
    """

    # ── Locators ──────────────────────────────────────────────────

    PAGE_TITLE = (By.CSS_SELECTOR, ".pageTitle")

    # Submenus
    BATCHES_MENU = (By.ID, "Active_31")
    PRE_BILLING_MENU = (By.ID, "Active_32")
    GENERAL_LEDGER_MENU = (By.ID, "Active_83")

    # Batches - Open Batches table
    BATCH_PROCESS_TABLE = (By.ID, "billingProcessTableID")
    BATCH_ROW_PREFIX = "trBillingBatch_"
    CREATE_BATCH_BTN = (By.CSS_SELECTOR, '[onclick="CreateBillBatch()"]')
    BILLING_CYCLE_SELECT2 = (By.CSS_SELECTOR, '[title="Select Billing Cycle"]')
    CREATE_NEW_BATCH_BTN = (By.CSS_SELECTOR, '[onclick="CreateNewBatch()"]')
    BILLED_THROUGH_DATE = (By.ID, "sBilledThroughDate")
    THREE_EYE_BLUE = (By.ID, "threeEyeBlue")
    PROCESS_BATCH_BTN = (By.CSS_SELECTOR, '[onclick^="processBillingHistory"]')
    YES_PROCEED_BTN = (By.CSS_SELECTOR, '[onclick="YesProceed()"]')
    FINALIZE_BATCH_BTN = (By.CSS_SELECTOR, '[onclick^="FinalizeBatchBillingProcess"]')
    FINALIZE_CONFIRM_BTN = (By.CSS_SELECTOR, '[onclick="FinalizeOrPostTransactionsBillingBatchProcess()"]')
    CLOSED_BATCHES_TAB = (By.CSS_SELECTOR, '[onclick="OpenBillingBatch(2)"]')
    LOAD_HISTORY_BTN = (By.CSS_SELECTOR, '[onclick="LoadBillHistoryGrid()"]')
    CLOSED_BATCH_GRID = (By.ID, "billingprocessListGrid")

    # Comparison
    VIEW_COMPARE_BATCH = (By.CSS_SELECTOR, '[onclick^="ViewCompareBatch("]')
    COMPARISON_BATCH_LINK = (By.CSS_SELECTOR, '[onclick^="setvaluesforbillingbatchcomparison"]')

    # Batch History
    VIEW_BATCH_COMPARISON = (By.CSS_SELECTOR, '[onclick^="ViewBatchComparison("]')
    VIEW_BATCH_COMPARISON_TITLE = (By.ID, "viewBatchComparisonTitle")

    # Transactions
    VIEW_BILLING_TRANSACTION = (By.CSS_SELECTOR, '[onclick^="ViewBillingTransaction("]')

    # Reports dropdown
    DATA_TOGGLE_DROPDOWN = (By.CSS_SELECTOR, '[data-toggle="dropdown"]')

    # Auto Pays
    SHOW_AUTO_PAYMENTS = (By.CSS_SELECTOR, '[onclick^="ShowBillingAutomaticPaymentPopUp("]')

    # Order History Report
    ORDER_HISTORY_TEMPLATE = (By.ID, "ddlOrderHistoryTemplate")
    RUN_ORDER_HISTORY_BTN = (By.ID, "btnRunOrderHistoryReport")

    # Void / Reverse
    VOID_POPUP_BTN = (By.CSS_SELECTOR, '[onclick^="ShowVoidPopUp"]')
    VOID_BATCH_BTN = (By.CSS_SELECTOR, '[onclick="VoidBillingBatch()"]')
    REVERSE_POPUP_BTN = (By.CSS_SELECTOR, '[onclick^="ShowReversePopUp"]')
    GO_REVERSE_BTN = (By.CSS_SELECTOR, '[onclick="GoReverse()"]')

    # Closed Batches tab (for download invoices)
    CLOSED_TAB_LINK = (By.CSS_SELECTOR, "#parentLiTab_2 a.nav-link")
    CLOSED_TAB_SEARCH_BTN = (By.CSS_SELECTOR, "#parentTabContainer_2 input.btn")
    DOWNLOAD_INVOICE_POPUP = (By.ID, "divDownloadInvoicePopup")

    # Pre-Billing
    BILLING_CYCLE_DROPDOWN = (By.ID, "ddlBillingCycle")
    PRE_BILLING_LOAD_BTN = (By.CSS_SELECTOR, '[onclick="GetBillingAuditsPartial();"]')
    VIEW_INCOMPLETE_ORDERS_BTN = (By.ID, "btnViewIncompleteOrders")
    PRE_BILLING_TAB2 = (By.CSS_SELECTOR, "#parentLiTab_2 span")
    AUDIT_SUMMARY_TABLE = (By.ID, "BillingAuditSummaryTable")
    AUDIT_SUMMARY_DETAIL_POPUP = (By.CSS_SELECTOR, "#BillingAuditSummaryDetailDisplayPopUp h5.modal-title")
    AUDIT_SUMMARY_DETAIL_TABLE_LINK = (By.CSS_SELECTOR, "#BillingAuditSummaryDetailTable td.serviceCode_td a")
    WORK_ORDER_LABEL = (By.ID, "myWorkOrderLabel")
    AUDIT_DETAIL_TABLE_SPAN = (By.CSS_SELECTOR, "#BillingAuditDetailTable span")

    # General Ledger
    GL_FILTER_TYPE = (By.ID, "ddlfiltertype")
    GL_DETAIL_DES = (By.ID, "ddlDetailDes")
    GL_LOAD_BTN = (By.CSS_SELECTOR, '[onclick="LoadLedgerExport()"]')
    GL_EXPORT_POPUP_BTN = (By.CSS_SELECTOR, '[onclick="ExportLedgerPopup()"]')
    GL_EXPORT_DETAIL_FILE = (By.CSS_SELECTOR, '[onclick="ExportLedgerCreateDetailFile()"]')
    GL_EXPORT_SUMMARY_FILE = (By.CSS_SELECTOR, '[onclick="ExportLedgerCreateFile()"]')
    GL_EXPORT_COMPLETE_BATCH = (By.CSS_SELECTOR, '[onclick="ExportLedgerCompleteBatch()"]')
    GL_PERIOD_INPUT = (By.CSS_SELECTOR, '[name="Period"]')
    GL_SEARCH_BTN_TAB1 = (By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
    GL_ROUTE_FILTER = (By.CSS_SELECTOR, "#parentTabContainer_1 a.form-control")
    GL_TAB2 = (By.CSS_SELECTOR, "#parentLiTab_2 span")
    GL_TAB2_SEARCH_BTN = (By.CSS_SELECTOR, "#parentTabContainer_2 a.btn-primary")
    GL_EXPORT_BATCH_HISTORY_TABLE = (By.ID, "ExportBatchHistoryID")
    GL_EXPORT_BATCH_BTN = (By.CSS_SELECTOR, "#divExportBatchbtn a:nth-child(1)")
    GL_EXPORT_POPUP_SUBMIT = (By.CSS_SELECTOR, "#ExportExcelofExportHistoryBatchPopup button.pull-right")
    GL_EXPORT_TYPE = (By.ID, "ddlExportType")
    GL_TEMPLATE_OPTIONS = (By.CSS_SELECTOR, "#glTemplateExportOptions svg.svg_stroke")
    GL_EXPORT_POPUP_CLOSE = (By.CSS_SELECTOR, "#ExportExcelofExportHistoryBatchPopup button.close")

    GL_TABLE = (By.CSS_SELECTOR, "#GeneralLedgerTable, .dx-datagrid")
    SUCCESS_MESSAGE = (By.ID, "divSucessContent")

    # ── Actions ───────────────────────────────────────────────────

    def open_batches(self):
        """Click Batches submenu."""
        self.click_element(*self.BATCHES_MENU)
        self.wait_for_loading_screen()

    def open_pre_billing(self):
        """Click Pre-Billing submenu."""
        self.click_element(*self.PRE_BILLING_MENU)
        self.wait_for_loading_screen()

    def open_general_ledger(self):
        """Click General Ledger submenu."""
        self.click_element(*self.GENERAL_LEDGER_MENU)
        self.wait_for_loading_screen()

    def get_page_title(self):
        """Return page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def get_success_message(self):
        """Return text of the success/error message banner."""
        return self.get_text(*self.SUCCESS_MESSAGE)

    def is_success_visible(self):
        """Return True if success message is visible."""
        return self.element_is_visible(*self.SUCCESS_MESSAGE)

    # ── Batch helpers ─────────────────────────────────────────────

    def get_batch_rows(self, timeout=15):
        """Return all non-detail batch rows from the open batches table."""
        table = self.find_element(By.ID, "billingProcessTableID", timeout=timeout)
        rows = table.find_elements(
            By.CSS_SELECTOR, 'tbody tr[id^="trBillingBatch_"]:not([id*="Detail"])'
        )
        return rows

    def find_14_day_row(self, status_filter=None, timeout=15):
        """
        Find a batch row containing '14 Day' text.
        Optionally filter by status text (e.g. 'Unbilled', 'Processed').
        Returns the row element or None.
        """
        rows = self.get_batch_rows(timeout=timeout)
        for row in rows:
            text = row.text
            if re.search(r'14\s*Day', text, re.IGNORECASE):
                if status_filter is None:
                    return row
                if status_filter.lower() in text.lower():
                    return row
        return None

    def get_batch_id_from_row(self, row):
        """Extract numeric batch ID from a row's cells."""
        cells = row.find_elements(By.TAG_NAME, "td")
        for cell in cells:
            text = cell.text.strip()
            if text and re.match(r'^\d+$', text):
                return text
        return None

    def click_three_eye_in_row(self, row):
        """Click the actions (three-eye) icon within a batch row."""
        icon = row.find_element(By.ID, "threeEyeBlue")
        self.driver.execute_script("arguments[0].click();", icon)

    def click_create_batch(self):
        """Click the Create Billing Batch button."""
        self.click_element(*self.CREATE_BATCH_BTN)
        self.wait_for_loading_screen()

    def select_billing_cycle_14(self):
        """Select '14 Day' billing cycle from Select2 dropdown."""
        self.click_element(*self.BILLING_CYCLE_SELECT2)
        search = self.find_visible(By.CSS_SELECTOR, '[class*="-search__field"]')
        search.send_keys("14")
        search.send_keys(Keys.ENTER)
        self.wait_for_loading_screen()

    def set_billing_dates(self):
        """Set billing date and billed-through date to today."""
        today = datetime.now().strftime("%m/%d/%Y")
        # Billing Date input
        billing_date_input = self.find_element(
            By.XPATH,
            "//label[contains(text(),'Billing Date')]/parent::*/descendant::input[1]"
        )
        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly'); arguments[0].value=''; arguments[0].value=arguments[1];",
            billing_date_input, today
        )
        billing_date_input.send_keys(Keys.TAB)

        # Billed Through Date
        billed_through = self.find_element(*self.BILLED_THROUGH_DATE)
        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly'); arguments[0].value=''; arguments[0].value=arguments[1];",
            billed_through, today
        )
        billed_through.send_keys(Keys.TAB)

    def click_create_new_batch(self):
        """Click the Create New Batch confirmation button."""
        self.click_element(*self.CREATE_NEW_BATCH_BTN)
        self.wait_for_loading_screen()

    def process_batch_from_row(self, row):
        """Click three-eye > Process on a batch row."""
        self.click_three_eye_in_row(row)
        self.find_clickable(
            By.CSS_SELECTOR, '[onclick^="processBillingHistory"]'
        ).click()

    def confirm_process_batch(self):
        """Confirm the process batch modal."""
        self.find_visible(
            By.XPATH,
            "//*[contains(text(),'Are you sure you want to process this batch and run billing?')]",
            timeout=10
        )
        self.click_element(*self.YES_PROCEED_BTN)
        self.wait_for_loading_screen()

    def open_first_batch_actions(self):
        """Open three-eye menu on first batch row."""
        table = self.find_element(By.ID, "billingProcessTableID", timeout=15)
        first_row = table.find_element(By.CSS_SELECTOR, 'tr[id^="trBillingBatch"]')
        self.click_three_eye_in_row(first_row)
        return first_row

    def cleanup_14_day_batches(self):
        """
        Remove any existing 14 Day batches via void/reverse so the test
        starts clean. Iterates until no 14 Day batches remain.
        """
        max_iterations = 10
        for _ in range(max_iterations):
            try:
                rows = self.get_batch_rows(timeout=5)
            except (TimeoutException, NoSuchElementException):
                return

            target_row = None
            action = None
            for row in rows:
                text = row.text or ""
                if not re.search(r'14\s*Day', text, re.IGNORECASE):
                    continue
                if 'Not processed' in text:
                    target_row = row
                    action = 'void_or_reverse'
                    break
                elif 'Unbilled' in text:
                    target_row = row
                    action = 'void'
                    break
                elif 'Processed' in text or 'PostTransactions' in text:
                    target_row = row
                    action = 'reverse_then_void'
                    break

            if target_row is None:
                return

            self.click_three_eye_in_row(target_row)

            if action == 'void':
                self._click_void_popup_and_confirm()
            elif action == 'void_or_reverse':
                self._void_or_reverse_from_dropdown()
            elif action == 'reverse_then_void':
                self._reverse_then_void()

            self.wait_for_loading_screen()

    def _click_void_popup_and_confirm(self):
        """Click void popup button then confirm."""
        try:
            self.find_clickable(
                By.CSS_SELECTOR, '[onclick^="ShowVoidPopUp"]', timeout=5
            ).click()
        except TimeoutException:
            pass
        try:
            self.find_clickable(
                By.CSS_SELECTOR, '[onclick="VoidBillingBatch()"]', timeout=5
            ).click()
        except TimeoutException:
            pass

    def _void_or_reverse_from_dropdown(self):
        """From an open dropdown, click Void if available, else Reverse then Void."""
        dropdown_links = self.driver.find_elements(
            By.CSS_SELECTOR,
            '.dropdown-content a, .dropdown-menu a, .billingcontentdropdown a, [class*="dropdown"] a'
        )
        has_void = any(re.search(r'void', el.text, re.IGNORECASE) for el in dropdown_links if el.is_displayed())
        has_reverse = any(re.search(r'reverse', el.text, re.IGNORECASE) for el in dropdown_links if el.is_displayed())

        if has_void:
            for el in dropdown_links:
                if re.search(r'void', el.text, re.IGNORECASE) and el.is_displayed():
                    self.driver.execute_script("arguments[0].click();", el)
                    break
            try:
                self.find_clickable(
                    By.CSS_SELECTOR, '[onclick="VoidBillingBatch()"]', timeout=5
                ).click()
            except TimeoutException:
                pass
        elif has_reverse:
            self._reverse_then_void()

    def _reverse_then_void(self):
        """Reverse a batch, then void it."""
        try:
            self.find_clickable(
                By.CSS_SELECTOR, '[onclick^="ShowReversePopUp"]', timeout=5
            ).click()
            self.find_clickable(
                By.CSS_SELECTOR, '[onclick="GoReverse()"]', timeout=5
            ).click()
            self.wait_for_loading_screen()
            # After reverse, find the 14 Day row again and void it
            row = self.find_14_day_row(timeout=10)
            if row:
                self.click_three_eye_in_row(row)
                self._click_void_popup_and_confirm()
        except TimeoutException:
            pass

    # ── General Ledger helpers ────────────────────────────────────

    def gl_select_filter_type(self, value):
        """Select GL filter type dropdown by value."""
        el = self.find_element(*self.GL_FILTER_TYPE)
        Select(el).select_by_value(str(value))

    def gl_select_detail_des(self, value):
        """Select GL detail description dropdown by value."""
        el = self.find_element(*self.GL_DETAIL_DES)
        Select(el).select_by_value(str(value))

    def gl_select_detail_des_by_index(self, index):
        """Select GL detail description dropdown by index."""
        el = self.find_element(*self.GL_DETAIL_DES)
        Select(el).select_by_index(index)

    def gl_click_load(self):
        """Click Load Ledger Export button."""
        self.click_element(*self.GL_LOAD_BTN)
        self.wait_for_loading_screen()

    def gl_select_checkbox(self, index=1):
        """Click a dx-checkbox in the grid by index."""
        checkboxes = self.find_elements(By.CSS_SELECTOR, ".dx-checkbox-container")
        if len(checkboxes) > index:
            checkboxes[index].click()

    def gl_click_export_popup(self):
        """Click Export Ledger Popup button."""
        self.click_element(*self.GL_EXPORT_POPUP_BTN)

    def gl_click_export_detail_file(self):
        """Click Export Detail File button."""
        self.click_element(*self.GL_EXPORT_DETAIL_FILE)
        self.wait_for_loading_screen()

    def gl_click_export_summary_file(self):
        """Click Export Summary File button."""
        self.click_element(*self.GL_EXPORT_SUMMARY_FILE)
        self.wait_for_loading_screen()

    def gl_click_complete_batch(self):
        """Click Export Complete Batch button."""
        self.click_element(*self.GL_EXPORT_COMPLETE_BATCH)
        self.wait_for_loading_screen()
