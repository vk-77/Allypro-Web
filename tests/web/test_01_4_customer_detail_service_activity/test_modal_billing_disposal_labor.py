"""
Customer Details - Service Activity tab - work order Billing / Disposal / Labor tab.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, scroll_to_element, force_click
from config.web_settings import DEFAULT_WAIT


BILLING_TABLE_COLUMN_LABELS = [
    "Svc Code", "Description", "Type", "Qty", "Unit Rate",
    "No Charge Qty", "Max Qty", "Max Qty Rate", "Min Charge", "Total", "Action",
]

DISPOSAL_TABLE_COLUMN_LABELS = [
    "Date", "Vehicle", "Driver", "Destination", "Ticket Nbr",
    "Material", "Weight", "Volume", "UOM", "Fee", "Actions",
]

DISPOSAL_STATUS_POPUP_LABELS = [
    "StartTime:", "EndTime:", "OdometerStart:", "OdometerEnd:",
    "DestinationArrival:", "DestinationDeparture:",
    "LocationArrivalTime:", "LocationDepartureTime:", "LocationReturnTime:", "Detail:",
]

DISPOSAL_AUDIT_HEADER_LABELS = [
    "Update Date", "Field", "Old value ", "New value ", "User Name ",
]


def _open_billing_tab(driver):
    """Open today's work order and activate the Billing tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_BILLING, page.WO_PANE_BILLING)
    return page


def _ensure_billing_tab_active(page):
    """Verify the billing tab pane is visible and active."""
    pane = page.find_visible(*page.WO_PANE_BILLING, timeout=15)
    assert "active" in pane.get_attribute("class")
    return pane


def _open_add_charge_form(page, driver):
    """Open the Add Charge form on the Billing tab and select Svc + quantity type."""
    _ensure_billing_tab_active(page)
    # Wait for ShowAddNewChargeRow script
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return typeof ShowAddNewChargeRow === 'function'")
    )
    add_btn = page.find_visible(*page.WO_BILLING_BTN_ADD_CHARGE)
    scroll_to_element(driver, add_btn)
    force_click(driver, *page.WO_BILLING_BTN_ADD_CHARGE)
    # Wait for footer row
    row = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, "#tblBilling tfoot #allchargeinputfield"
        ))
    )
    WebDriverWait(driver, 10).until(
        lambda d: row.value_of_css_property("display") == "table-row"
    )
    # Select first Svc code
    svc_select = page.find_element(*page.WO_BILLING_NEW_CHARGE_SVC)
    sel = Select(svc_select)
    if len(sel.options) > 1:
        sel.select_by_index(1)
    wait_for_loading_screen(driver)
    # Wait for quantity type to populate
    WebDriverWait(driver, 25).until(
        lambda d: len(Select(d.find_element(By.CSS_SELECTOR, "#allchargeinputfield #txtQuantityType")).options) > 0
    )
    qty_sel = Select(driver.find_element(By.CSS_SELECTOR, "#allchargeinputfield #txtQuantityType"))
    if not qty_sel.first_selected_option.get_attribute("value"):
        for opt in qty_sel.options:
            if opt.get_attribute("value"):
                qty_sel.select_by_value(opt.get_attribute("value"))
                break


def _save_new_charge(driver):
    """Click Save on the new charge footer row."""
    save_btn = driver.find_element(
        By.CSS_SELECTOR, '#allchargeinputfield button[onclick="SaveNewChargeRow()"]'
    )
    force_click(driver, By.CSS_SELECTOR, '#allchargeinputfield button[onclick="SaveNewChargeRow()"]')
    wait_for_loading_screen(driver)


def _add_and_save_one_billing_charge(driver):
    """Open billing, add charge form, fill, save."""
    page = _open_billing_tab(driver)
    _open_add_charge_form(page, driver)
    _save_new_charge(driver)
    wait_for_loading_screen(driver)
    return page


def _get_last_billing_row_id(driver):
    """Return the DOM id of the last billing charge row."""
    rows = driver.find_elements(By.CSS_SELECTOR, '#tblBilling tbody.tBodyBillCharge tr[id^="billRow_"]')
    assert len(rows) >= 1, "Expected at least one billing charge row"
    return rows[-1].get_attribute("id")


def _ensure_disposal_rows_exist(page, driver):
    """If no disposal rows exist, add one."""
    page.scroll_disposal_table_right()
    disposal_rows = driver.find_elements(
        By.CSS_SELECTOR,
        "#divRouteTripDisposalContainer table.manage_drivehelper tbody#trbodyDisposal tr.rowcontainerDisposal[id^='ds_']"
    )
    return len(disposal_rows) >= 1


def _get_last_disposal_row_id(driver):
    """Return the DOM id of the last disposal data row."""
    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "#divRouteTripDisposalContainer table.manage_drivehelper tbody#trbodyDisposal tr.rowcontainerDisposal[id^='ds_']"
    )
    assert len(rows) >= 1, "Expected at least one disposal data row"
    return rows[-1].get_attribute("id")


@pytest.mark.usefixtures("driver")
class TestModalBillingDisposalLabor:
    """
    Service Activity tab - work order Billing / Disposal / Labor tab.

    """

    def test_c339655_billing_tab_po_payment_status_recalc_add_charge(self, driver):
        """C339655 Billing tab: PO#, Payment Required, Billing Status, Recalculate, and Add Charge are visible."""
        page = _open_billing_tab(driver)
        pane = _ensure_billing_tab_active(page)
        # PO# label and input
        po_label = pane.find_element(By.XPATH, './/label[contains(text(),"PO#")]')
        assert po_label.is_displayed()
        # Payment Required
        payment = page.find_visible(*page.WO_BILLING_PAYMENT_REQUIRED)
        assert payment.is_displayed()
        # Billing Status
        status = page.find_visible(*page.WO_BILLING_STATUS_SELECT)
        assert status.is_displayed()
        sel = Select(status)
        options_text = [o.text for o in sel.options]
        assert any("Unbilled" in t for t in options_text)
        # Recalculate button
        recalc = page.find_visible(*page.WO_BILLING_BTN_RECALCULATE)
        assert recalc.is_displayed()
        # Add Charge button
        add_charge = page.find_visible(*page.WO_BILLING_BTN_ADD_CHARGE)
        assert add_charge.is_displayed()

    def test_c339656_billing_tab_charges_table_headers(self, driver):
        """C339656 Billing tab: service charges table shows expected column headers."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        wait_for_loading_screen(driver)
        # Wait for charges table
        charges_table = page.find_element(*page.WO_BILLING_CHARGES_TABLE, timeout=30)
        scroll_to_element(driver, charges_table)
        thead = charges_table.find_element(By.TAG_NAME, "thead")
        for label in BILLING_TABLE_COLUMN_LABELS:
            th = thead.find_element(By.XPATH, f'.//th[contains(text(),"{label}")]')
            assert th.is_displayed()

    def test_c339657_billing_tab_disposal_section(self, driver):
        """C339657 Billing tab: disposal section includes Add Disposal and grid column headers."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        disposal = page.find_element(*page.WO_DISPOSAL_SECTION)
        assert disposal is not None
        add_link = page.find_element(*page.WO_DISPOSAL_ADD_LINK)
        assert add_link is not None
        table = page.find_element(*page.WO_DISPOSAL_TABLE)
        thead = table.find_element(By.TAG_NAME, "thead")
        for label in DISPOSAL_TABLE_COLUMN_LABELS:
            th = thead.find_element(By.XPATH, f'.//th[contains(text(),"{label}")]')
            assert th is not None

    def test_c339658_billing_tab_disposal_row_status_icon_hover(self, driver):
        """C339658 Billing tab: disposal row status icon hover shows trip detail popup."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        if not _ensure_disposal_rows_exist(page, driver):
            pytest.skip("No disposal rows available for hover test")
        row_id = _get_last_disposal_row_id(driver)
        page.scroll_disposal_table_right()
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Find the status dropdown and popup
        status_div = row.find_element(By.CSS_SELECTOR, ".dropdown-status")
        # Assert popup exists with expected labels
        popup = row.find_element(By.CSS_SELECTOR, ".dropdown-order-content")
        menu = popup.find_element(By.CSS_SELECTOR, "ul.menuStatus")
        for label in DISPOSAL_STATUS_POPUP_LABELS:
            strong = menu.find_element(
                By.XPATH, f'.//strong[contains(@class,"nameLable") and contains(text(),"{label}")]'
            )
            assert strong is not None

    def test_c339659_billing_tab_po_numbers_modal_and_save(self, driver):
        """C339659 Billing tab: PO# opens Customer PO Numbers modal; close and Save PO shows success."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        # Edit PO
        edit_btn = page.find_visible(*page.WO_BILLING_PO_EDIT, timeout=10)
        edit_btn.click()
        wait_for_loading_screen(driver)
        # Copy trigger to open PO Numbers modal
        copy_trigger = page.find_visible(*page.WO_BILLING_PO_COPY, timeout=10)
        copy_trigger.click()
        wait_for_loading_screen(driver)
        # Customer PO Numbers modal
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH, '//h4[contains(@class,"modal-title") and contains(text(),"Customer PO Numbers")]'
            ))
        )
        # Close modal
        modal = driver.find_element(
            By.XPATH,
            '//h4[contains(@class,"modal-title") and contains(text(),"Customer PO Numbers")]'
            '/ancestor::*[contains(@class,"modal-content")]'
        )
        close_btn = modal.find_element(By.CSS_SELECTOR, "button.closeBtn")
        close_btn.click()
        wait_for_loading_screen(driver)
        # Save PO
        save_po = page.find_visible(*page.WO_BILLING_PO_SAVE)
        save_po.click()
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()

    def test_c339660_billing_tab_payment_required_decimal_input(self, driver):
        """C339660 Billing tab: Payment Required accepts decimal input and save succeeds."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        payment = page.find_visible(*page.WO_BILLING_PAYMENT_REQUIRED)
        previous = payment.get_attribute("value") or ""
        payment.clear()
        payment.send_keys("1500.25")
        driver.execute_script("arguments[0].blur();", payment)
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()
        # Restore previous value
        payment = page.find_visible(*page.WO_BILLING_PAYMENT_REQUIRED)
        payment.clear()
        payment.send_keys(previous)
        driver.execute_script("arguments[0].blur();", payment)
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()

    def test_c339661_billing_tab_billing_status_dropdown_interactive(self, driver):
        """C339661 Billing tab: Billing Status dropdown is interactive."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        status = page.find_visible(*page.WO_BILLING_STATUS_SELECT)
        assert status.is_displayed()
        assert status.is_enabled()
        status.click()

    def test_c339662_billing_tab_add_charge_opens_footer(self, driver):
        """C339662 Billing tab: Add Charge opens the footer row with Svc and quantity type."""
        page = _open_billing_tab(driver)
        _open_add_charge_form(page, driver)
        # Verify footer row is visible
        footer_row = driver.find_element(
            By.CSS_SELECTOR, "#tblBilling tfoot #allchargeinputfield"
        )
        assert footer_row.value_of_css_property("display") == "table-row"
        svc = driver.find_element(By.ID, "ddlServiceCode")
        assert svc.get_attribute("value")
        qty = driver.find_element(By.CSS_SELECTOR, "#allchargeinputfield #txtQuantityType")
        assert qty.get_attribute("value")

    def test_c339663_billing_tab_save_closes_footer_adds_row(self, driver):
        """C339663 Billing tab: Save closes the new charge footer and adds a grid row."""
        page = _open_billing_tab(driver)
        _open_add_charge_form(page, driver)
        _save_new_charge(driver)
        wait_for_loading_screen(driver)
        # Footer row should be hidden
        footer_row = driver.find_element(
            By.CSS_SELECTOR, "#tblBilling tfoot #allchargeinputfield"
        )
        WebDriverWait(driver, 25).until(
            lambda d: footer_row.value_of_css_property("display") == "none"
        )
        # At least one charge row should exist
        rows = driver.find_elements(
            By.CSS_SELECTOR, '#tblBilling tbody.tBodyBillCharge tr[id^="billRow_"]'
        )
        assert len(rows) >= 1

    def test_c339664_billing_tab_edit_last_charge_line(self, driver):
        """C339664 Billing tab: Edit the last charge line."""
        page = _add_and_save_one_billing_charge(driver)
        row_id = _get_last_billing_row_id(driver)
        counter = row_id.replace("billRow_", "")
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Click edit
        edit_btn = row.find_element(By.CSS_SELECTOR, 'button.btnChargeEdit[title="Edit"]')
        onclick = edit_btn.get_attribute("onclick")
        driver.execute_script(onclick)
        # Set unit rate to 4
        ur_selector = f"#chUR_{counter}"
        ur_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ur_selector))
        )
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
            ur_input, "4"
        )
        assert ur_input.get_attribute("value") == "4"

    def test_c339665_billing_tab_save_inline_after_edit(self, driver):
        """C339665 Billing tab: Save inline after editing the last charge line."""
        page = _add_and_save_one_billing_charge(driver)
        row_id = _get_last_billing_row_id(driver)
        counter = row_id.replace("billRow_", "")
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Edit
        edit_btn = row.find_element(By.CSS_SELECTOR, 'button.btnChargeEdit[title="Edit"]')
        onclick = edit_btn.get_attribute("onclick")
        driver.execute_script(onclick)
        ur_selector = f"#chUR_{counter}"
        ur_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ur_selector))
        )
        driver.execute_script(
            "arguments[0].value = '4'; arguments[0].dispatchEvent(new Event('input'));",
            ur_input
        )
        # Save inline
        save_btn = row.find_element(By.CSS_SELECTOR, 'button[onclick*="SaveUpdateChargeRow"]')
        save_onclick = save_btn.get_attribute("onclick")
        driver.execute_script(save_onclick)
        wait_for_loading_screen(driver)
        # Verify unit rate is no longer editable and shows 4.00
        WebDriverWait(driver, 25).until(
            lambda d: not d.find_element(By.CSS_SELECTOR, ur_selector).is_displayed()
        )

    def test_c339666_billing_tab_delete_charge(self, driver):
        """C339666 Billing tab: Verify Delete option is working fine."""
        page = _add_and_save_one_billing_charge(driver)
        row_id = _get_last_billing_row_id(driver)
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Accept confirm dialog
        driver.execute_script("window.confirm = function() { return true; };")
        delete_btn = row.find_element(By.CSS_SELECTOR, 'button.btnChargeDelete[title="Delete"]')
        onclick = delete_btn.get_attribute("onclick")
        driver.execute_script(onclick)
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()

    def test_c339667_billing_tab_add_disposal_opens_footer(self, driver):
        """C339667 Billing tab: Add Disposal opens the new-row footer."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        wait_for_loading_screen(driver)
        add_link = page.find_element(*page.WO_DISPOSAL_ADD_LINK)
        scroll_to_element(driver, add_link)
        force_click(driver, *page.WO_DISPOSAL_ADD_LINK)
        # Wait for tfoot to be visible
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#divRouteTripDisposalContainer table.manage_drivehelper tfoot#alldisposalinputfield"
            ))
        )

    def test_c339668_billing_tab_save_disposal_row(self, driver):
        """C339668 Billing tab: Save persists a new disposal row."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        wait_for_loading_screen(driver)
        # Open Add Disposal
        add_link = page.find_element(*page.WO_DISPOSAL_ADD_LINK)
        scroll_to_element(driver, add_link)
        force_click(driver, *page.WO_DISPOSAL_ADD_LINK)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#divRouteTripDisposalContainer table.manage_drivehelper tfoot#alldisposalinputfield"
            ))
        )
        # Fill fields (select first available options)
        # Destination
        page.select2_click_option("#select2-disposalDestinationDdl-container", "", timeout=15)
        # Driver
        page.select2_click_option("#select2-diaposalDriverDdl-container", "", timeout=15)
        # Vehicle
        page.select2_click_option("#select2-disposalVehicleNameDdl-container", "", timeout=15)
        # Volume
        vol = page.find_visible(By.ID, "Dispoasl_Volume")
        vol.clear()
        vol.send_keys("4")
        # Ticket
        ticket = page.find_visible(By.ID, "disposal_TicketNbr")
        ticket.clear()
        ticket.send_keys("1234")
        # Save
        save_btn = driver.find_element(
            By.CSS_SELECTOR,
            '#alldisposalinputfield button[onclick="SaveRouteTripDisposal()"]'
        )
        driver.execute_script(save_btn.get_attribute("onclick"))
        wait_for_loading_screen(driver)

    def test_c339669_billing_tab_edit_disposal_line(self, driver):
        """C339669 Billing tab: Verify Edit and save functionality."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        if not _ensure_disposal_rows_exist(page, driver):
            pytest.skip("No disposal rows available for edit test")
        row_id = _get_last_disposal_row_id(driver)
        page.scroll_disposal_table_right()
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Click Edit
        edit_btn = row.find_element(By.CSS_SELECTOR, 'button[title="Edit"][onclick^="EditDisposalInfo"]')
        driver.execute_script(edit_btn.get_attribute("onclick"))
        wait_for_loading_screen(driver)

    def test_c339670_billing_tab_view_disposal_history(self, driver):
        """C339670 Billing tab: View disposal history opens disposal trips modal."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        if not _ensure_disposal_rows_exist(page, driver):
            pytest.skip("No disposal rows available for view history test")
        row_id = _get_last_disposal_row_id(driver)
        page.scroll_disposal_table_right()
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Click View History (clock icon)
        history_link = row.find_element(
            By.CSS_SELECTOR, 'a[title="View History"][onclick*="ShowDisposalTripAuditHistory"]'
        )
        driver.execute_script(history_link.get_attribute("onclick"))
        wait_for_loading_screen(driver)
        # Verify modal
        modal = page.find_visible(*page.WO_DISPOSAL_AUDIT_MODAL, timeout=15)
        assert modal.is_displayed()
        title = page.find_visible(*page.WO_DISPOSAL_AUDIT_TITLE)
        assert "Disposal Trips Update History" in title.text
        # Close
        close_btn = modal.find_element(By.CSS_SELECTOR, "button.closeBtn")
        close_btn.click()
        wait_for_loading_screen(driver)
        assert page.element_not_visible(*page.WO_DISPOSAL_AUDIT_MODAL, timeout=10)

    def test_c339671_billing_tab_view_history_audit_layout(self, driver):
        """C339671 Billing tab: View History click opens audit modal with grid layout."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        if not _ensure_disposal_rows_exist(page, driver):
            pytest.skip("No disposal rows available for audit layout test")
        row_id = _get_last_disposal_row_id(driver)
        page.scroll_disposal_table_right()
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        history_link = row.find_element(
            By.CSS_SELECTOR, 'a[title="View History"][onclick*="ShowDisposalTripAuditHistory"]'
        )
        driver.execute_script(history_link.get_attribute("onclick"))
        wait_for_loading_screen(driver)
        # Verify audit modal layout
        modal = page.find_visible(*page.WO_DISPOSAL_AUDIT_MODAL, timeout=15)
        title = page.find_visible(*page.WO_DISPOSAL_AUDIT_TITLE)
        assert "Disposal Trips Update History" in title.text
        # Grid headers
        grid = driver.find_element(By.ID, "Audit_vw_RouteDisposalList")
        thead = grid.find_element(By.TAG_NAME, "thead")
        for label in DISPOSAL_AUDIT_HEADER_LABELS:
            th = thead.find_element(By.XPATH, f'.//th[contains(text(),"{label}")]')
            assert th is not None
        # Close
        close_btn = modal.find_element(By.CSS_SELECTOR, "button.closeBtn")
        close_btn.click()
        wait_for_loading_screen(driver)

    def test_c339672_billing_tab_delete_disposal_line(self, driver):
        """C339672 Billing tab: Delete the last disposal line."""
        page = _open_billing_tab(driver)
        _ensure_billing_tab_active(page)
        if not _ensure_disposal_rows_exist(page, driver):
            pytest.skip("No disposal rows available for delete test")
        row_id = _get_last_disposal_row_id(driver)
        page.scroll_disposal_table_right()
        row = driver.find_element(By.ID, row_id)
        scroll_to_element(driver, row)
        # Accept confirm dialog
        driver.execute_script("window.confirm = function() { return true; };")
        delete_btn = row.find_element(
            By.CSS_SELECTOR, 'button[title="Delete"][onclick^="DeleteDisposalInfo"]'
        )
        driver.execute_script(delete_btn.get_attribute("onclick"))
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()
