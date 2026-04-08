"""
Receivables - Payment Batches tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.receivables_page import ReceivablesPage
from helpers.web_helper import (
    click_submenu,
    wait_for_loading_screen,
    select_date_range,
    scroll_to_element,
    force_click,
)
from data.dataload import dates


@pytest.mark.usefixtures("driver")
class TestPaymentBatches:
    """
    Verify Payment Batches grid, filters, clear, actions, and details.

    Usage:
        pytest tests/web/test_08_receivables/test_01_payment_batches.py -v
    """

    def _navigate_to_payment_batches(self, driver):
        """Navigate to Receivables > Payment Batches."""
        page = ReceivablesPage(driver)
        page.open_payment_batches()
        return page

    def _click_load(self, driver):
        """Click the Load button and wait for loading."""
        wait = WebDriverWait(driver, 10)
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[onclick="LoadData();"]')
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

    def test_c69985_grid_columns_are_displayed_correctly(self, driver):
        """C69985 Grid columns are displayed correctly."""
        self._navigate_to_payment_batches(driver)

        # Load data first to ensure table is rendered
        self._click_load(driver)

        wait = WebDriverWait(driver, 10)

        # Validate table exists
        wait.until(EC.presence_of_element_located(
            (By.ID, "paymentBatchTable")
        ))

        # Validate all expected grid columns exist in the table header
        expected_columns = [
            "Batch ID", "Batch Date", "Type", "Source",
            "Description", "Status", "Records", "Amount",
            "Created", "Actions",
        ]
        for col in expected_columns:
            header = driver.find_element(
                By.XPATH,
                f'//table[@id="paymentBatchTable"]//th[contains(text(),"{col}")]'
            )
            assert header is not None, f"Column header '{col}' should exist"

    def test_c69986_load_button_displays_data_in_grid(self, driver):
        """C69986 Load button displays data in grid."""
        self._navigate_to_payment_batches(driver)

        # Click Load button
        self._click_load(driver)

        wait = WebDriverWait(driver, 10)

        # Validate grid exists
        wait.until(EC.presence_of_element_located(
            (By.ID, "paymentBatchTable")
        ))

        # Check if at least one row exists, otherwise expect "No record" message
        tbody = driver.find_element(By.ID, "DispatchBodyRowContainer")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        if len(rows) > 0:
            assert rows[0].is_displayed(), (
                "First data row should be visible"
            )
        else:
            assert driver.find_element(
                By.XPATH, "//*[contains(text(),'No record')]"
            ).is_displayed(), "No record message should be visible"

    def test_c69987_filters_are_working_correctly(self, driver):
        """C69987 Filters are working correctly."""
        self._navigate_to_payment_batches(driver)

        # Set date range filter
        select_date_range(
            driver, "txtFromDate", "txtToDate",
            dates["d5_days_ago"], dates["today"],
        )

        # Select Type filter if available
        type_selects = driver.find_elements(
            By.CSS_SELECTOR, '#ddlType, [name*="Type"], select[id*="type"]'
        )
        if type_selects:
            el = type_selects[0]
            options = el.find_elements(By.TAG_NAME, "option")
            if len(options) > 1:
                Select(el).select_by_index(1)

        # Select Status filter if available
        status_selects = driver.find_elements(
            By.CSS_SELECTOR, '#ddlStatus, [name*="Status"], select[id*="status"]'
        )
        if status_selects:
            el = status_selects[0]
            options = el.find_elements(By.TAG_NAME, "option")
            if len(options) > 1:
                Select(el).select_by_index(1)

        # Select Source filter if available
        source_selects = driver.find_elements(
            By.CSS_SELECTOR, '#ddlSource, [name*="Source"], select[id*="source"]'
        )
        if source_selects:
            el = source_selects[0]
            options = el.find_elements(By.TAG_NAME, "option")
            if len(options) > 1:
                Select(el).select_by_index(1)

        # Click Load to apply filters
        self._click_load(driver)

        # Validate results updated
        assert driver.find_element(By.ID, "paymentBatchTable"), (
            "Payment batch table should exist after filtering"
        )

    def test_c69988_clear_button_resets_filters(self, driver):
        """C69988 Clear button resets filters."""
        self._navigate_to_payment_batches(driver)

        wait = WebDriverWait(driver, 10)

        # Load data first
        self._click_load(driver)

        # Select rows if available
        tbody = driver.find_element(By.ID, "DispatchBodyRowContainer")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        if len(rows) > 0:
            checkboxes = driver.find_elements(
                By.CSS_SELECTOR, ".chkInvoiceTransactions"
            )
            if checkboxes:
                driver.execute_script("arguments[0].click();", checkboxes[0])

        # Enable Group Digital toggle
        chk_group = driver.find_element(By.ID, "chkGroupDigital")
        if not chk_group.is_selected():
            driver.execute_script("arguments[0].click();", chk_group)
        assert chk_group.is_selected(), "Group Digital should be checked"

        # Get default date values
        default_from = driver.find_element(By.ID, "txtFromDate").get_attribute("value")
        default_to = driver.find_element(By.ID, "txtToDate").get_attribute("value")

        # Set custom date range
        select_date_range(
            driver, "txtFromDate", "txtToDate",
            dates["d5_days_ago"], dates["today"],
        )

        # Verify date was changed
        from_val = driver.find_element(By.ID, "txtFromDate").get_attribute("value")
        to_val = driver.find_element(By.ID, "txtToDate").get_attribute("value")
        assert from_val == dates["d5_days_ago"], "From date should be set"
        assert to_val == dates["today"], "To date should be set"

        # Click Load to apply filter
        self._click_load(driver)

        # Click Clear button
        clear_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[onclick="ClearData();"]')
        ))
        clear_btn.click()
        wait_for_loading_screen(driver)

        # Validate Group Digital is unchecked
        chk_group = driver.find_element(By.ID, "chkGroupDigital")
        assert not chk_group.is_selected(), "Group Digital should be unchecked after clear"

        # Validate selected rows are unchecked
        checkboxes = driver.find_elements(By.CSS_SELECTOR, ".chkInvoiceTransactions")
        for chk in checkboxes:
            assert not chk.is_selected(), "Row checkboxes should be unchecked after clear"

        # Validate dates are reset (not equal to the custom value we set)
        cleared_from = driver.find_element(By.ID, "txtFromDate").get_attribute("value")
        cleared_to = driver.find_element(By.ID, "txtToDate").get_attribute("value")
        assert cleared_from != dates["d5_days_ago"], "From date should be reset"
        assert cleared_from, "From date should not be empty"
        assert cleared_to != dates["d5_days_ago"], "To date should be reset"
        assert cleared_to, "To date should not be empty"

    def test_c69989_action_icons_are_clickable(self, driver):
        """C69989 Action icons are clickable."""
        self._navigate_to_payment_batches(driver)

        # Load data first
        self._click_load(driver)

        tbody = driver.find_element(By.ID, "DispatchBodyRowContainer")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        if len(rows) > 0:
            first_row = rows[0]
            # Look for action buttons in first row
            action_links = first_row.find_elements(
                By.CSS_SELECTOR,
                '.printActionOuter a, .print a, '
                '[data-original-title*="Print"], '
                '[data-original-title*="Export"], '
                'a[href*="PaymentBatchDetail"]'
            )
            assert len(action_links) > 0, "Action icons should exist in first row"
            scroll_to_element(driver, action_links[0])
            assert action_links[0].is_displayed(), "Action icon should be visible"
            assert action_links[0].is_enabled(), "Action icon should be enabled"
        else:
            pytest.skip("No data available to test action icons")

    def test_c69990_empty_results_display_correctly(self, driver):
        """C69990 Empty results display correctly."""
        self._navigate_to_payment_batches(driver)

        # Set date range to very old range
        select_date_range(
            driver, "txtFromDate", "txtToDate",
            "01/01/2000", "01/01/2001",
        )

        # Apply filters
        self._click_load(driver)

        # Validate empty state
        tbody = driver.find_element(By.ID, "DispatchBodyRowContainer")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        if len(rows) > 0:
            # Should contain "No data available in table" message
            assert "No data available in table" in tbody.text, (
                "Empty results should show 'No data available in table'"
            )
        else:
            assert len(rows) == 0, "Table should be empty"

    def test_c69991_view_details_action_opens_details_view(self, driver):
        """C69991 View/Details action opens details view."""
        self._navigate_to_payment_batches(driver)

        # Load data first
        self._click_load(driver)

        wait = WebDriverWait(driver, 15)

        tbody = driver.find_element(By.ID, "DispatchBodyRowContainer")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        if len(rows) > 0:
            first_row = rows[0]

            # Find detail link and remove target attribute so it opens in same window
            detail_link = first_row.find_element(
                By.CSS_SELECTOR, 'a[href*="PaymentBatchDetail"]'
            )
            scroll_to_element(driver, detail_link)
            driver.execute_script(
                "arguments[0].removeAttribute('target');", detail_link
            )
            driver.execute_script("arguments[0].click();", detail_link)

            wait_for_loading_screen(driver)

            # Validate details page opened
            page_title = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "p.pageTitle")
            ))
            assert "Payment Batch Details" in page_title.text, (
                "Page title should contain 'Payment Batch Details'"
            )

            # Validate Batch # label is visible
            assert driver.find_element(
                By.XPATH, "//*[contains(text(),'Batch #:')]"
            ).is_displayed(), "Batch # label should be visible"

            # Validate Back button exists
            back_btn = driver.find_element(
                By.XPATH,
                "//a[contains(@class,'btn') and contains(@class,'btn-secondary') "
                "and contains(text(),'Back')]"
            )
            assert back_btn.is_displayed(), "Back button should be visible"
        else:
            pytest.skip("No data available to test view action")
