"""
Receivables - Receivables Management tests.

Validates filters, template save, add activity, add adjustment,
status change, statement creation, email statement, send message,
and export functionality on the Receivables Management page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.receivables_page import ReceivablesPage
from helpers.web_helper import (
    wait_for_loading_screen,
    force_click,
)


@pytest.mark.usefixtures("driver")
class TestReceivablesManagement:
    """
    Verify Receivables Management: filters, templates, activities,
    adjustments, status changes, statements, email, messaging, and export.

    Usage:
        pytest tests/web/receivables/test_receivables_management.py -v
    """

    def _navigate_to_receivables_management(self, driver):
        """Navigate to Receivables > Receivables Management."""
        page = ReceivablesPage(driver)
        page.open_receivables_management()
        return page

    def _click_filter_submit(self, driver):
        """Click the filter submit button (13th li > a.btn)."""
        wait = WebDriverWait(driver, 10)
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content li:nth-child(13) a.btn")
        ))
        submit_btn.click()

    def _select_billing_cycle_14day(self, driver):
        """Open billing cycle filter and select '14 Day'."""
        wait = WebDriverWait(driver, 10)

        # Click billing cycle filter dropdown
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content span.hideBillingCycle")
        )).click()

        # Select '14 Day' checkbox
        label = wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             "//li[contains(@class,'nth-of-type') or ancestor::li[position()=3]]"
             "//label[contains(@class,'checkbox')]"
             "[ancestor::*[@id='routeListContainer']]"
             "[.//input[@value='14 Day']]"
             " | "
             "//li[3]//div[@id='routeListContainer']//li[3]//label[contains(@class,'checkbox')]"
             )
        ))
        label.click()

        checkbox = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="14 Day"]'
        )
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)

    def _apply_billing_cycle_14day_filter(self, driver):
        """Select 14 Day billing cycle and click filter submit."""
        wait = WebDriverWait(driver, 10)

        # Click billing cycle expander
        billing_expander = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content span.hideBillingCycle")
        ))
        billing_expander.click()

        # Click the 3rd li label inside routeListContainer under 3rd li group
        label = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "li:nth-of-type(3) #routeListContainer li:nth-child(3) > label.checkbox"
        )))
        label.click()

        # Ensure checkbox is checked
        checkbox = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="14 Day"]'
        )
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)

        # Click filter submit
        self._click_filter_submit(driver)
        wait_for_loading_screen(driver)

    def _select_first_data_row(self, driver):
        """Click the first data row checkbox (dx-checkbox)."""
        wait = WebDriverWait(driver, 10)
        checkbox = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[class="dx-checkbox-container"]')
        ))
        # Click the second checkbox (index 1) as in original test
        checkboxes = driver.find_elements(
            By.CSS_SELECTOR, '[class="dx-checkbox-container"]'
        )
        if len(checkboxes) > 1:
            checkboxes[1].click()
        else:
            checkboxes[0].click()

    def test_c67620_filters_are_working(self, driver):
        """C67620 Filters are working."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Click submit without filters - expect error
        self._click_filter_submit(driver)
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Please select at least one Filter" in success_msg.text, (
            "Should show filter required message"
        )

        # Open customer status filter and select option
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content li:nth-child(1) a.form-control")
        )).click()

        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#content div.mutliSelectCustomerStatus li:nth-child(2) label.checkbox"
        ))).click()

        checkbox = driver.find_element(
            By.CSS_SELECTOR, '#content input[value="1"]'
        )
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)

        # Submit filters
        self._click_filter_submit(driver)
        wait_for_loading_screen(driver)

        wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))

        # Open Customer Class filter
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content span.hideCustomerClass")
        )).click()

        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "li:nth-of-type(2) #routeListContainer li:nth-child(3) label.checkbox"
        ))).click()

        chk_class = driver.find_element(
            By.CSS_SELECTOR,
            "#routeListContainer li:nth-child(3) input.chkCustomerClass"
        )
        if not chk_class.is_selected():
            driver.execute_script("arguments[0].click();", chk_class)

        # Open billing cycle filter
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content li:nth-child(3) a.form-control")
        )).click()

        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "li:nth-of-type(3) #routeListContainer li:nth-child(5) label.checkbox"
        ))).click()

        chk_billing = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="28 days"]'
        )
        if not chk_billing.is_selected():
            driver.execute_script("arguments[0].click();", chk_billing)

        # Open Invoice Delivery filter
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content span.hideInvoiceDelivery")
        )).click()

        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "li:nth-of-type(4) #routeListContainer li:nth-child(3) label.checkbox"
        ))).click()

        chk_delivery = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="Email invoice"]'
        )
        if not chk_delivery.is_selected():
            driver.execute_script("arguments[0].click();", chk_delivery)

        # Submit filters
        self._click_filter_submit(driver)
        wait_for_loading_screen(driver)

        # Set finance charge and aging bucket
        Select(driver.find_element(By.ID, "ddlfinancecharge")).select_by_value("1")
        Select(driver.find_element(By.ID, "ddlAgingBucket")).select_by_value("AgeBal0")

        self._click_filter_submit(driver)

        # Set arithmetic and balance
        Select(driver.find_element(By.ID, "ddlArithmetic")).select_by_visible_text(
            "Greater than"
        )
        balance_field = driver.find_element(By.ID, "txtBalance")
        balance_field.click()
        balance_field.clear()
        balance_field.send_keys("1")

        # Select collection template
        Select(driver.find_element(
            By.CSS_SELECTOR, '[name="ddlAgingCollectionTemplate"]'
        )).select_by_value("4f95affc-3988-46c0-bea9-6bf75650939a")

        self._click_filter_submit(driver)
        wait_for_loading_screen(driver)

    def test_c67621_save_template_is_working(self, driver):
        """C67621 Save Template is working."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Click template filter label
        wait.until(EC.element_to_be_clickable(
            (By.ID, "TFilterLabel")
        )).click()

        # Type template name
        template_name = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[name="AgingCollectionTemplateName"]')
        ))
        template_name.click()
        template_name.clear()
        template_name.send_keys("test")

        # Check and uncheck VisibleToAll
        visible_all = driver.find_element(
            By.CSS_SELECTOR, '[name="VisibleToAll"]'
        )
        if not visible_all.is_selected():
            driver.execute_script("arguments[0].click();", visible_all)
        driver.execute_script("arguments[0].click();", visible_all)

        # Click save
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnTemplateSave")
        )).click()

        # Validate success message
        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        )).is_displayed(), "Success message should be visible"

    def test_c67622_add_activity_is_working(self, driver):
        """C67622 Add Activity is working."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Apply 14 Day billing cycle filter
        self._apply_billing_cycle_14day_filter(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click Add Activity button (1st button in divAgincollectionStatus)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(1) > button.btn")
        )).click()
        wait_for_loading_screen(driver)

        # Select activity type via Select2
        wait.until(EC.element_to_be_clickable(
            (By.ID, "select2-Svc_ATabDDlType-container")
        )).click()

        # Select first CALL option
        call_option = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[id*="-CALL"]')
        ))
        driver.execute_script("arguments[0].click();", call_option)

        # Type contact name
        contact = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[name="Svc_ATabContact"]')
        ))
        contact.click()
        contact.clear()
        contact.send_keys("RandomName")

        # Click save activity
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#cTabActivityAgingcustomerPopUpBody input.btn-primary")
        )).click()
        wait_for_loading_screen(driver)

        # Validate second button is visible (activity was added)
        assert wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(2) > button.btn")
        )).is_displayed(), "Second action button should be visible"

    def test_c67623_add_adjustment_is_working(self, driver):
        """C67623 Add Adjustment is working."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Open billing cycle and select 14 Day
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content li:nth-child(3) a.form-control")
        )).click()

        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "li:nth-of-type(3) #routeListContainer li:nth-child(3) > label.checkbox"
        ))).click()

        chk = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="14 Day"]'
        )
        if not chk.is_selected():
            driver.execute_script("arguments[0].click();", chk)

        self._click_filter_submit(driver)
        wait_for_loading_screen(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click Add Adjustment button (2nd div button)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(2) > button.btn")
        )).click()

        # Click save without rate - expect error
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnSaveAddAdjustment")
        )).click()

        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Unit Rate should not be equal to zero" in success_msg.text, (
            "Should show unit rate error"
        )

        # Enter unit rate
        rate_field = driver.find_element(By.ID, "txtAddAdjustmentUnitRate")
        rate_field.click()
        rate_field.clear()
        rate_field.send_keys("12")

        # Verify AppearOnInvoice is checked
        appear_chk = driver.find_element(
            By.CSS_SELECTOR, '[name="chkAddAdjustmentAppearonInvoice"]'
        )
        assert appear_chk.is_selected(), "Appear on Invoice should be checked"

        # Save adjustment
        driver.find_element(By.ID, "btnSaveAddAdjustment").click()

        # Select row again
        self._select_first_data_row(driver)

        # Validate success message
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Adjustment has been saved successfully" in success_msg.text, (
            "Should show adjustment saved message"
        )

    def test_c67624_change_status(self, driver):
        """C67624 Change Status."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Open billing cycle and select 14 Day
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content li:nth-child(3) a.form-control")
        )).click()

        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "li:nth-of-type(3) #routeListContainer li:nth-child(3) > label.checkbox"
        ))).click()

        chk = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="14 Day"]'
        )
        if not chk.is_selected():
            driver.execute_script("arguments[0].click();", chk)

        self._click_filter_submit(driver)
        wait_for_loading_screen(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click Change Status button (3rd div button)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(3) > button.btn")
        )).click()

        # Select status
        Select(driver.find_element(
            By.CSS_SELECTOR, '[name="Cust_Sett_CustomerStatusId"]'
        )).select_by_value("1")

        # Verify popup header is visible
        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "cTabActivityAgingCustomerstatusPopUpHeader")
        )).is_displayed(), "Status popup header should be visible"

        # Click save button
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#myCTabAddAgingcustomerstatusBody a.btn")
        )).click()
        wait_for_loading_screen(driver)

        # Verify popup is closed
        assert wait.until(EC.invisibility_of_element_located(
            (By.ID, "cTabActivityAgingCustomerstatusPopUpHeader")
        )), "Status popup should be closed"

    def test_c67625_create_statement(self, driver):
        """C67625 Create Statement."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Apply 14 Day billing cycle filter
        self._apply_billing_cycle_14day_filter(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click Create Statement button (4th div button)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(4) button.btn")
        )).click()

        # Verify create statement popup is visible
        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "cTabCreateStatementPopUpHeader")
        )).is_displayed(), "Create Statement popup should be visible"

        # Select invoice format
        invoice_format = driver.find_element(
            By.CSS_SELECTOR, '[name="InvoiceFormat"]'
        )
        Select(invoice_format).select_by_index(1)

        # Click download statement
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnDownloadStatement")
        )).click()

        # Verify success message
        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        )).is_displayed(), "Success message should be visible"

        # Verify download queue button
        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "btnStatementDownloadQueue")
        )).is_displayed(), "Download queue button should be visible"

        # Click History tab
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#parentLiTabHistory_2 a")
        )).click()

        # Verify history grid header
        assert wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#tRefundAuditGrid th:nth-child(1)")
        )).is_displayed(), "History grid header should be visible"

        # Verify popup still visible
        assert driver.find_element(
            By.ID, "cTabCreateStatementPopUpHeader"
        ).is_displayed(), "Create Statement popup should still be visible"

        # Close the popup
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "div:nth-of-type(7) #myCTabAddEditNotePopUp button.close")
        )).click()

        # Verify popup is closed
        assert wait.until(EC.invisibility_of_element_located(
            (By.ID, "cTabCreateStatementPopUpHeader")
        )), "Create Statement popup should be closed"

    def test_c67626_email_statement(self, driver):
        """C67626 Email Statement."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Apply 14 Day billing cycle filter
        self._apply_billing_cycle_14day_filter(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click Email Statement button (5th div button)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(5) button.btn")
        )).click()

        # Select invoice format
        Select(driver.find_element(
            By.CSS_SELECTOR, '[name="InvoiceFormat"]'
        )).select_by_index(1)

        # Click email statement
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnEmailStatement")
        )).click()

        # Verify success message
        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        )).is_displayed(), "Success message should be visible"

        # Verify email queue button text
        email_queue_btn = wait.until(EC.presence_of_element_located(
            (By.ID, "btnStatementEmailQueue")
        ))
        assert "Email is in queue" in email_queue_btn.text, (
            "Email queue button should show 'Email is in queue'"
        )

        # Close the popup
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "div:nth-of-type(8) #myCTabAddEditNotePopUp button.close")
        )).click()

    def test_c67627_send_message(self, driver):
        """C67627 Send Message."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Apply 14 Day billing cycle filter
        self._apply_billing_cycle_14day_filter(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click Send Message button (6th div button)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divAgincollectionStatus div:nth-child(6) > button.btn")
        )).click()

        # Select message type
        Select(driver.find_element(By.ID, "ddlSendMessageType")).select_by_value("1")

        # Select message template
        Select(driver.find_element(
            By.ID, "ddlSendMessageTemplate"
        )).select_by_value("24")

        # Verify modal header is visible
        assert wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#modalSendMessagePopup div.modal-header h4.modal-title")
        )).is_displayed(), "Send Message modal should be visible"

        # Click Next
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnCommonNext")
        )).click()

        # Verify SMS and AutoCall are not checked
        sms_chk = driver.find_element(
            By.CSS_SELECTOR, '[name="chkSendMessageSMSActive"]'
        )
        assert not sms_chk.is_selected(), "SMS should not be checked"

        auto_call_chk = driver.find_element(
            By.CSS_SELECTOR, '[name="chkSendMessageAutoCallActive"]'
        )
        assert not auto_call_chk.is_selected(), "AutoCall should not be checked"

        # Check Email
        email_chk = driver.find_element(
            By.CSS_SELECTOR, '[name="chkSendMessageEmailActive"]'
        )
        if not email_chk.is_selected():
            driver.execute_script("arguments[0].click();", email_chk)

        # Click Edit Before Send
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnEditBeforeSend")
        )).click()

        # Verify form label is visible
        assert wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#tab1Table div:nth-child(6) label.form-label")
        )).is_displayed(), "Form label should be visible"

        # Click Send Now
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnCommonSendNow")
        )).click()

        # Verify process started message
        assert wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(text(),"
            "'Process has been started. Will notify you when completed.')]"
        ))).is_displayed(), "Process started message should be visible"

        assert wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        )).is_displayed(), "Success message should be visible"

    def test_c67628_export(self, driver):
        """C67628 Export."""
        self._navigate_to_receivables_management(driver)

        wait = WebDriverWait(driver, 10)

        # Apply 14 Day billing cycle filter
        self._apply_billing_cycle_14day_filter(driver)

        # Select first data row
        self._select_first_data_row(driver)

        # Click export (Excel) button
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#btnExcel svg.svg_fill")
        )).click()
        wait_for_loading_screen(driver)
