"""
Receivables page object for Payment Batches, Auto Apply, and Management.

Covers batch loading, auto-apply operations, receivables templates,
statements, messaging, and data export.
"""
from selenium.webdriver.common.by import By

from .base_web_page import BasePage


class ReceivablesPage(BasePage):
    """Page object for Payment Batches, Auto Apply, and Receivables Management."""

    # ── Locators ──────────────────────────────────────────────────

    # Submenus
    PAYMENT_BATCHES_MENU = (By.ID, "Active_61")
    AUTO_APPLY_MENU = (By.ID, "Active_66")
    RECEIVABLES_MGMT_MENU = (By.ID, "Active_62")

    # Payment Batches
    PAYMENT_BATCH_TABLE = (By.CSS_SELECTOR, "#PaymentBatchTable, .dx-datagrid")
    ADD_BATCH_BTN = (By.CSS_SELECTOR, '[onclick*="AddBatch"], #btnAddBatch')

    # Auto Apply
    BILLING_CYCLE_SELECT2 = (By.ID, "select2-ddlBillingCycle-container")
    BILLING_CYCLE_DROPDOWN = (By.ID, "ddlBillingCycle")
    LOAD_BTN = (By.CSS_SELECTOR, '[onclick="LoadPaymentCredit()"]')
    CLEAR_BTN = (By.CSS_SELECTOR, '[onclick="clearFilter()"]')
    AUTO_APPLY_BTN = (By.ID, "btnAutoApply")
    PAYMENT_CREDIT_TABLE = (By.ID, "paymentCreditTable")
    DISPATCH_BODY_ROWS = (By.CSS_SELECTOR, "#DispatchBodyRowContainer tr")
    NO_RECORD_MSG = (By.CSS_SELECTOR, ".norecord1")

    # Auto Apply modal
    REVERSE_MODAL = (By.ID, "myReverseModal-container")
    AUTO_APPLY_CONFIRM_BTN = (By.CSS_SELECTOR, "#myReverseModal-container #btnAutoApplyPaymentCredit")

    # Payment Batches grid
    PAYMENT_BATCH_TABLE_BY_ID = (By.ID, "paymentBatchTable")
    LOAD_DATA_BTN = (By.CSS_SELECTOR, '[onclick="LoadData();"]')
    CLEAR_DATA_BTN = (By.CSS_SELECTOR, '[onclick="ClearData();"]')
    DISPATCH_BODY_CONTAINER = (By.ID, "DispatchBodyRowContainer")
    GROUP_DIGITAL_CHK = (By.ID, "chkGroupDigital")
    FROM_DATE = (By.ID, "txtFromDate")
    TO_DATE = (By.ID, "txtToDate")

    # Receivables Management
    FILTER_SUBMIT_BTN = (By.CSS_SELECTOR, "#content li:nth-child(13) a.btn")
    TEMPLATE_LABEL = (By.ID, "TFilterLabel")
    TEMPLATE_SAVE_BTN = (By.ID, "btnTemplateSave")
    TEMPLATE_NAME_INPUT = (By.CSS_SELECTOR, '[name="AgingCollectionTemplateName"]')
    VISIBLE_TO_ALL_CHK = (By.CSS_SELECTOR, '[name="VisibleToAll"]')
    DX_CHECKBOX_CONTAINERS = (By.CSS_SELECTOR, '[class="dx-checkbox-container"]')
    BILLING_CYCLE_EXPANDER = (By.CSS_SELECTOR, "#content span.hideBillingCycle")
    CUSTOMER_CLASS_EXPANDER = (By.CSS_SELECTOR, "#content span.hideCustomerClass")
    INVOICE_DELIVERY_EXPANDER = (By.CSS_SELECTOR, "#content span.hideInvoiceDelivery")
    FINANCE_CHARGE_SELECT = (By.ID, "ddlfinancecharge")
    AGING_BUCKET_SELECT = (By.ID, "ddlAgingBucket")
    ARITHMETIC_SELECT = (By.ID, "ddlArithmetic")
    BALANCE_INPUT = (By.ID, "txtBalance")
    COLLECTION_TEMPLATE_SELECT = (By.CSS_SELECTOR, '[name="ddlAgingCollectionTemplate"]')

    # Add Adjustment
    SAVE_ADJUSTMENT_BTN = (By.ID, "btnSaveAddAdjustment")
    UNIT_RATE_INPUT = (By.ID, "txtAddAdjustmentUnitRate")
    APPEAR_ON_INVOICE_CHK = (By.CSS_SELECTOR, '[name="chkAddAdjustmentAppearonInvoice"]')

    # Change Status
    CUSTOMER_STATUS_SELECT = (By.CSS_SELECTOR, '[name="Cust_Sett_CustomerStatusId"]')
    STATUS_POPUP_HEADER = (By.ID, "cTabActivityAgingCustomerstatusPopUpHeader")

    # Create Statement
    CREATE_STATEMENT_POPUP = (By.ID, "cTabCreateStatementPopUpHeader")
    INVOICE_FORMAT_SELECT = (By.CSS_SELECTOR, '[name="InvoiceFormat"]')
    DOWNLOAD_STATEMENT_BTN = (By.ID, "btnDownloadStatement")
    DOWNLOAD_QUEUE_BTN = (By.ID, "btnStatementDownloadQueue")

    # Email Statement
    EMAIL_STATEMENT_BTN = (By.ID, "btnEmailStatement")
    EMAIL_QUEUE_BTN = (By.ID, "btnStatementEmailQueue")

    # Send Message
    SEND_MSG_TYPE_SELECT = (By.ID, "ddlSendMessageType")
    SEND_MSG_TEMPLATE_SELECT = (By.ID, "ddlSendMessageTemplate")
    SEND_MSG_NEXT_BTN = (By.ID, "btnCommonNext")
    SEND_MSG_SEND_NOW_BTN = (By.ID, "btnCommonSendNow")
    EDIT_BEFORE_SEND_BTN = (By.ID, "btnEditBeforeSend")

    # Export
    EXPORT_EXCEL_BTN = (By.CSS_SELECTOR, "#btnExcel svg.svg_fill")

    SUCCESS_MESSAGE = (By.ID, "divSucessContent")

    # ── Actions ───────────────────────────────────────────────────

    def open_payment_batches(self):
        """Click Payment Batches submenu."""
        self.click_element(*self.PAYMENT_BATCHES_MENU)
        self.wait_for_loading_screen()

    def open_auto_apply(self):
        """Click Auto Apply submenu."""
        self.click_element(*self.AUTO_APPLY_MENU)
        self.wait_for_loading_screen()

    def open_receivables_management(self):
        """Click Receivables Management submenu."""
        self.click_element(*self.RECEIVABLES_MGMT_MENU)
        self.wait_for_loading_screen()

    def get_success_message(self):
        """Return success/error message text."""
        return self.get_text(*self.SUCCESS_MESSAGE)

    def is_success_visible(self):
        """Return True if success message is visible."""
        return self.element_is_visible(*self.SUCCESS_MESSAGE)
