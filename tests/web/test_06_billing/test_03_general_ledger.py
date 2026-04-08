"""
Billing - General Ledger Export tests.

"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.billing_page import BillingPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select_date_range,
    select_dropdown_by_index,
    force_click,
)
from config.web_settings import BASE_URL


@pytest.mark.usefixtures("driver")
class TestGeneralLedger:
    """
    Billing > General Ledger Export tests.

    Usage:
        pytest tests/web/test_06_billing/test_03_general_ledger.py -v
    """

    def _open_general_ledger(self, driver):
        """Navigate to Billing > General Ledger Export."""
        page = BillingPage(driver)
        page.open_general_ledger()
        assert page.text_is_visible("General Ledger Export"), (
            "General Ledger Export heading should be visible"
        )
        return page

    def _setup_gl_filter_and_load(self, driver, page):
        """Common setup: select filter type 1, detail des 1, set date range, load."""
        page.gl_select_filter_type("1")
        page.gl_select_detail_des_by_index(1)
        select_date_range(driver, "txtFromDateLedger", "txtToDateLedger",
                          _default_from(), _default_to())
        page.gl_click_load()

    # ── C60372 ────────────────────────────────────────────────────

    def test_c60372_export_details_file(self, driver):
        """C60372 Export Details File."""
        page = self._open_general_ledger(driver)
        self._setup_gl_filter_and_load(driver, page)

        page.gl_select_checkbox(index=1)
        page.gl_click_export_popup()
        page.gl_click_export_detail_file()

    # ── C60373 ────────────────────────────────────────────────────

    def test_c60373_export_summary_file(self, driver):
        """C60373 Export Summary File."""
        page = self._open_general_ledger(driver)
        self._setup_gl_filter_and_load(driver, page)

        page.gl_select_checkbox(index=1)
        page.gl_click_export_popup()
        page.gl_click_export_summary_file()

    # ── C60374 ────────────────────────────────────────────────────

    def test_c60374_complete_batch(self, driver):
        """C60374 Complete batch."""
        page = self._open_general_ledger(driver)
        self._setup_gl_filter_and_load(driver, page)

        page.gl_select_checkbox(index=1)
        page.gl_click_export_popup()
        page.gl_click_complete_batch()

    # ── C67618 ────────────────────────────────────────────────────

    def test_c67618_export_from_export_batch_tab(self, driver):
        """C67618 Export from Export Batch Tab."""
        page = self._open_general_ledger(driver)

        # Select filter type 2
        page.gl_select_filter_type("2")
        wait_for_loading_screen(driver)

        # Switch to Export Batch tab (tab 2)
        page.click_element(By.CSS_SELECTOR, "#parentLiTab_2 span")

        # Set date range for batch history
        select_date_range(
            driver, "txtFromDateBatchHistory", "txtToDateBatchHistory",
            _default_from(), _default_to()
        )

        # Click search
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_2 a.btn-primary")
        wait_for_loading_screen(driver)

        # Check first export batch row
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                '#ExportBatchHistoryID tr:nth-child(1) [name="chkExportBatchID"]'
            ))
        )
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", checkbox)

        # Click export button
        page.click_element(By.CSS_SELECTOR, "#divExportBatchbtn a:nth-child(1)")

        # Click submit in export popup (first time - default export)
        page.click_element(
            By.CSS_SELECTOR,
            "#ExportExcelofExportHistoryBatchPopup button.pull-right"
        )
        wait_for_loading_screen(driver)

        # Select export type 2 and submit
        export_type = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ddlExportType"))
        )
        Select(export_type).select_by_value("2")
        page.click_element(
            By.CSS_SELECTOR,
            "#ExportExcelofExportHistoryBatchPopup button.pull-right"
        )
        wait_for_loading_screen(driver)

        # Open template options, uncheck Description and DebitAccount
        force_click(
            driver, By.CSS_SELECTOR, "#glTemplateExportOptions svg.svg_stroke"
        )
        chk_desc = driver.find_element(By.ID, "chk_Description")
        if chk_desc.is_selected():
            driver.execute_script("arguments[0].click();", chk_desc)
        chk_debit = driver.find_element(By.ID, "chk_DebitAccount")
        if chk_debit.is_selected():
            driver.execute_script("arguments[0].click();", chk_debit)

        page.click_element(
            By.CSS_SELECTOR,
            "#ExportExcelofExportHistoryBatchPopup button.pull-right"
        )
        wait_for_loading_screen(driver)

        # Select export type 4, uncheck fields, submit
        export_type = driver.find_element(By.ID, "ddlExportType")
        Select(export_type).select_by_value("4")

        chk_gl_desc = driver.find_element(By.ID, "chk_GLAccountDescription")
        if chk_gl_desc.is_selected():
            driver.execute_script("arguments[0].click();", chk_gl_desc)
        chk_record = driver.find_element(By.ID, "chk_RecordCount")
        if chk_record.is_selected():
            driver.execute_script("arguments[0].click();", chk_record)

        page.click_element(
            By.CSS_SELECTOR,
            "#ExportExcelofExportHistoryBatchPopup button.pull-right"
        )

        # Close popup
        page.click_element(
            By.CSS_SELECTOR,
            "#ExportExcelofExportHistoryBatchPopup button.close"
        )

    # ── C67619 ────────────────────────────────────────────────────

    def test_c67619_test_filters_and_multiple_reports_type(self, driver):
        """C67619 Test filters and multiple reports type."""
        page = self._open_general_ledger(driver)

        # Set period to 5
        period_input = page.find_clickable(By.CSS_SELECTOR, '[name="Period"]')
        period_input.click()
        period_input.clear()
        period_input.send_keys("5")

        # Click search (tab 1)
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#dx-col-9 div.dx-datagrid-text-content"
        ), "Grid column 9 should be visible after search"

        # Open route filter, check value 0
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.form-control")
        checkbox_0 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '#routeListContainer input[value="0"]'
            ))
        )
        if not checkbox_0.is_selected():
            driver.execute_script("arguments[0].click();", checkbox_0)

        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#dx-col-24 div.dx-datagrid-text-content"
        ), "Grid column 24 should be visible"

        # Change detail description to 2
        page.gl_select_detail_des("2")
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)

        # Change filter type to 2
        page.gl_select_filter_type("2")
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#dx-col-54 div.dx-datagrid-text-content"
        ), "Grid column 54 should be visible"

        # Change detail description to 3
        page.gl_select_detail_des("3")
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#dx-col-66 div.dx-datagrid-text-content"
        ), "Grid column 66 should be visible"

        # Open route filter, click 2nd label, uncheck value 0
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.form-control")
        page.click_element(
            By.CSS_SELECTOR, "#routeListContainer li:nth-child(2) label.checkbox"
        )
        checkbox_0 = driver.find_element(
            By.CSS_SELECTOR, '#routeListContainer input[value="0"]'
        )
        if checkbox_0.is_selected():
            driver.execute_script("arguments[0].click();", checkbox_0)

        # Detail description 5
        page.gl_select_detail_des("5")
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(By.ID, "dx-col-81"), (
            "Grid column 81 should be visible"
        )

        # Detail description 4
        page.gl_select_detail_des("4")
        page.click_element(By.CSS_SELECTOR, "#parentTabContainer_1 a.btn-primary")
        wait_for_loading_screen(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#dx-col-98 div.dx-datagrid-text-content"
        ), "Grid column 98 should be visible"


def _default_from():
    """Return default from-date for GL date range (uses dataload)."""
    from data.dataload import dates
    return dates["one_month_ago"]


def _default_to():
    """Return default to-date for GL date range (uses dataload)."""
    from data.dataload import dates
    return dates["today"]
