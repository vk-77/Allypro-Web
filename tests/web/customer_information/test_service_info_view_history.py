"""
Customer Details - Service Info dropdown View History tests.

Validates the View History modal displays customer and location details,
service history grid data, and column headers.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.web.base_web_page import BasePage
from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    scroll_to_element,
    force_click,
)
from data.user_data import USER_DATA
from data.service_info_data import SERVICE_INFO_DATA


@pytest.mark.usefixtures("driver")
class TestServiceInfoViewHistory:
    """
    Service Info dropdown - View History option tests.

    Usage:
        pytest tests/web/customer_information/test_service_info_view_history.py -v
    """

    def test_c70531_view_history_opens_modal_with_customer_location(self, driver):
        """C70531 View History - Clicking opens modal and displays customer and location details."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.add_new_service_from_customer_details()
        page.open_service_info_view_history()

        # Assert modal title contains "View History" and "Service ID"
        label = wait.until(
            EC.visibility_of_element_located((By.ID, "myMapViewLabel"))
        )
        assert "View History" in label.text, f"Expected 'View History' in '{label.text}'"
        assert "Service ID" in label.text, f"Expected 'Service ID' in '{label.text}'"

        # Customer/location container visible with non-empty names
        cust_loc = driver.find_element(By.ID, "divCustLocContainer")
        assert cust_loc.is_displayed()

        cust_name = driver.find_element(By.ID, "settingsCustName")
        assert cust_name.is_displayed()
        assert cust_name.text.strip() != ""

        cust_loc_name = driver.find_element(By.ID, "settingsCustLocation")
        assert cust_loc_name.is_displayed()
        assert cust_loc_name.text.strip() != ""

        # Assert customer and location contain the customer ID
        customer_id = str(USER_DATA.get("customer_id", ""))
        if customer_id:
            assert customer_id in cust_name.text, f"Customer name should contain '{customer_id}'"
            assert customer_id in cust_loc_name.text, f"Customer location should contain '{customer_id}'"

        # Close popup
        close_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "btnServicePopupClose"))
        )
        scroll_to_element(driver, close_btn)
        driver.execute_script("arguments[0].click();", close_btn)

    def test_c70533_view_history_edit_service_info_and_rollback(self, driver):
        """C70533 View History - Edit Service Info, verify changes, and rollback to original state."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.open_service_info_view_history()

        # Wait for history container
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "#HistoryMapPopupContainer, #divCustomerServiceChangeHistory"
        )))

        # Click Edit button in #divSurchargeIcon
        surcharge_div = wait.until(
            EC.visibility_of_element_located((By.ID, "divSurchargeIcon"))
        )
        edit_btn = surcharge_div.find_element(By.CSS_SELECTOR, 'button[title="Edit"]')
        scroll_to_element(driver, edit_btn)
        driver.execute_script("arguments[0].click();", edit_btn)

        # Wait for EDIT SERVICE INFO modal
        edit_modal = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[contains(@class,'modal')][.//text()[contains(translate(., 'edit service info', 'EDIT SERVICE INFO'), 'EDIT SERVICE INFO')]]"
            ))
        )

        # Click Service Information tab
        svc_tab_link = edit_modal.find_element(By.CSS_SELECTOR, 'a[href="#ServiceInformationTab"]')
        scroll_to_element(driver, svc_tab_link)
        driver.execute_script("arguments[0].click();", svc_tab_link)
        WebDriverWait(driver, 8).until(
            lambda d: "active" in d.find_element(By.ID, "ServiceInformationTab").get_attribute("class")
        )

        # Phase 1: Capture original values
        rate_field = driver.find_element(By.ID, "txtEditServiceRate")
        snap_rate = rate_field.get_attribute("value")

        rental_field = driver.find_element(By.ID, "txtEditRentalRate")
        snap_rental_rate = rental_field.get_attribute("value")

        term_type_select = driver.find_element(By.ID, "ddlEditTermType")
        snap_term_type = term_type_select.get_attribute("value")

        snap_term_days = ""
        if snap_term_type == "0":
            try:
                term_days_field = driver.find_element(By.ID, "txtEditTermDays")
                snap_term_days = term_days_field.get_attribute("value")
            except NoSuchElementException:
                pass

        assert snap_rate is not None
        assert snap_term_type is not None

        # Phase 2: Edit with test data
        data = SERVICE_INFO_DATA.get("stage", {
            "rate": "2", "rental_rate": "5", "term_type": "0", "days": "5"
        })
        edit_rate = str(data.get("rate", "2"))
        edit_rental = str(data.get("rental_rate", "3"))
        edit_term_type = str(data.get("term_type", "0"))
        edit_days = str(data.get("days", "5"))

        rate_field.clear()
        rate_field.send_keys(edit_rate)

        if edit_rental:
            rental_field.clear()
            rental_field.send_keys(edit_rental)

        if edit_term_type:
            from selenium.webdriver.support.ui import Select
            Select(term_type_select).select_by_value(edit_term_type)

        if edit_term_type == "0" and edit_days:
            try:
                days_field = driver.find_element(By.ID, "txtEditTermDays")
                days_field.clear()
                days_field.send_keys(edit_days)
            except NoSuchElementException:
                pass

        # Click Update
        update_btn = edit_modal.find_element(By.CSS_SELECTOR, 'input.btn-primary[value="Update"]')
        assert update_btn.is_displayed()
        driver.execute_script("arguments[0].click();", update_btn)

        # Wait for modal to close
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((
                By.XPATH, "//div[contains(@class,'modal')][.//text()[contains(translate(., 'edit service info', 'EDIT SERVICE INFO'), 'EDIT SERVICE INFO')]]"
            ))
        )

        # Phase 3: Rollback - reopen edit and restore original values
        surcharge_div2 = wait.until(
            EC.visibility_of_element_located((By.ID, "divSurchargeIcon"))
        )
        edit_btn2 = surcharge_div2.find_element(By.CSS_SELECTOR, 'button[title="Edit"]')
        scroll_to_element(driver, edit_btn2)
        driver.execute_script("arguments[0].click();", edit_btn2)

        edit_modal2 = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[contains(@class,'modal')][.//text()[contains(translate(., 'edit service info', 'EDIT SERVICE INFO'), 'EDIT SERVICE INFO')]]"
            ))
        )

        svc_tab2 = edit_modal2.find_element(By.CSS_SELECTOR, 'a[href="#ServiceInformationTab"]')
        scroll_to_element(driver, svc_tab2)
        driver.execute_script("arguments[0].click();", svc_tab2)
        WebDriverWait(driver, 8).until(
            lambda d: "active" in d.find_element(By.ID, "ServiceInformationTab").get_attribute("class")
        )

        # Restore rate
        rate_restore = driver.find_element(By.ID, "txtEditServiceRate")
        rate_restore.clear()
        if snap_rate:
            rate_restore.send_keys(snap_rate)

        # Restore rental rate
        rental_restore = driver.find_element(By.ID, "txtEditRentalRate")
        rental_restore.clear()
        if snap_rental_rate:
            rental_restore.send_keys(snap_rental_rate)

        # Restore term type
        from selenium.webdriver.support.ui import Select
        term_type_val = snap_term_type if snap_term_type in ("0", "1") else "1"
        Select(driver.find_element(By.ID, "ddlEditTermType")).select_by_value(term_type_val)

        # Restore term days if applicable
        if term_type_val == "0" and snap_term_days:
            try:
                days_restore = driver.find_element(By.ID, "txtEditTermDays")
                days_restore.clear()
                days_restore.send_keys(snap_term_days)
            except NoSuchElementException:
                pass

        # Click Update to rollback
        update_btn2 = edit_modal2.find_element(By.CSS_SELECTOR, 'input.btn-primary[value="Update"]')
        driver.execute_script("arguments[0].click();", update_btn2)

        # Close View History popup
        close_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnServicePopupClose"))
        )
        scroll_to_element(driver, close_btn)
        driver.execute_script("arguments[0].click();", close_btn)

    def test_c70534_view_info_icon_opens_popup(self, driver):
        """C70534 View info icon opens popup."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 10)

        page.open_service_info_view_history()

        # Assert history has rows
        history_div = wait.until(
            EC.visibility_of_element_located((By.ID, "divCustomerServiceChangeHistory"))
        )
        table = history_div.find_element(
            By.CSS_SELECTOR, "#al-tableOuter, table.al-ServiceInfoList, table.table-bordered"
        )
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(rows) >= 1, "History table should have at least 1 row"

        # Click info icon in #divSurchargeIcon
        surcharge_div = wait.until(
            EC.visibility_of_element_located((By.ID, "divSurchargeIcon"))
        )
        info_icon = surcharge_div.find_element(By.CSS_SELECTOR, "a.servicemapicon.dropdown-toggle")
        assert info_icon.is_displayed()
        driver.execute_script("arguments[0].click();", info_icon)

    def test_c70535_view_history_routing_tab(self, driver):
        """C70535 View History - Routing tab opens, displays table, and shows headers."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 10)

        page.open_service_info_view_history()
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "#HistoryMapPopupContainer, #divCustomerServiceChangeHistory"
        )))

        # Click Routing tab
        tab_container = driver.find_element(By.ID, "parentTabContainerHistory")
        routing_link = tab_container.find_element(By.XPATH, ".//a[contains(text(),'Routing')]")
        assert routing_link.is_displayed()
        driver.execute_script("arguments[0].click();", routing_link)

        # Validate Routing tab is active
        routing_tab = WebDriverWait(driver, 8).until(
            lambda d: d.find_element(By.ID, "parentTabContainerHistory_2")
        )
        assert "active" in routing_tab.get_attribute("class")

        # Validate routing table and headers
        routing_table = wait.until(
            EC.visibility_of_element_located((By.ID, "tServiceInfoRoutingList"))
        )
        popup = driver.find_element(By.ID, "HistoryMapPopupContainer")
        headers = popup.find_elements(By.CSS_SELECTOR, "#tServiceInfoRoutingList thead th")
        header_texts = [h.text for h in headers]
        for expected in ["Date", "User", "Source", "End Date", "Start Date", "Routing"]:
            assert any(expected in ht for ht in header_texts), (
                f"Header '{expected}' not found in routing table"
            )

        # Close popup
        close_btn = driver.find_element(By.ID, "btnServicePopupClose")
        driver.execute_script("arguments[0].click();", close_btn)

    def test_c70536_view_charges_modal_and_table_headers(self, driver):
        """C70536 View Charges - click View Charges icon, validate Service Charges modal and table headers."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 10)

        page.open_service_info_view_history()

        # Click View Charges button in #divSurchargeIcon
        surcharge_div = wait.until(
            EC.visibility_of_element_located((By.ID, "divSurchargeIcon"))
        )
        charges_btn = surcharge_div.find_element(
            By.CSS_SELECTOR,
            'button[onclick*="GetSurChagesServiceDetails"], [data-original-title="View Charges"]'
        )
        assert charges_btn.is_displayed()
        driver.execute_script("arguments[0].click();", charges_btn)

        # Validate modal header
        header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "cViewDefaultchargePopUpHeader"))
        )
        assert "Service Charges" in header.text

        # Validate body visible
        body = driver.find_element(By.ID, "cViewDefaultchargeBody")
        assert body.is_displayed()

        # Validate table headers in #SurchargesTab
        surcharges_tab = driver.find_element(By.ID, "SurchargesTab")
        th_elements = surcharges_tab.find_elements(By.CSS_SELECTOR, "th")
        th_texts = [th.text for th in th_elements]
        for expected in ["Type", "Svc Code", "Charge Code", "Rate Type", "Default Qty", "Unit Rate"]:
            assert any(expected in ht for ht in th_texts), (
                f"Header '{expected}' not found in surcharges table"
            )

        # Close Service Charges modal
        close_btn = driver.find_element(
            By.CSS_SELECTOR, 'button[onclick*="HideViewDefaultcharge"]'
        )
        driver.execute_script("arguments[0].click();", close_btn)

        # Close View History popup
        popup_close = driver.find_element(By.ID, "btnServicePopupClose")
        driver.execute_script("arguments[0].click();", popup_close)

    def test_c70537_view_history_delete_icon_process_reversal(self, driver):
        """C70537 View History - Delete icon opens confirmation modal and Process Reversal completes."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 10)

        page.open_service_info_view_history()

        # Assert history has rows
        history_div = wait.until(
            EC.visibility_of_element_located((By.ID, "divCustomerServiceChangeHistory"))
        )
        table = history_div.find_element(
            By.CSS_SELECTOR, "#al-tableOuter, table.al-ServiceInfoList, table.table-bordered"
        )
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(rows) >= 1

        # Click Delete button
        surcharge_div = wait.until(
            EC.visibility_of_element_located((By.ID, "divSurchargeIcon"))
        )
        delete_btn = surcharge_div.find_element(
            By.CSS_SELECTOR, 'button[title="Delete"], button.deleteBtn'
        )
        assert delete_btn.is_displayed()
        driver.execute_script("arguments[0].click();", delete_btn)

        # Confirm Service Reverse modal
        confirm_modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[contains(@class,'modal')][.//*[contains(text(),'Confirm Service Reverse') or contains(text(),'CONFIRM SERVICE REVERSE')]]"
            ))
        )

        process_btn = driver.find_element(By.ID, "btnProcessReverseService")
        assert process_btn.is_displayed()
        assert "PROCESS REVERSAL" in process_btn.text.upper()
        driver.execute_script("arguments[0].click();", process_btn)

        # Validate UPDATE RESULT modal with success message
        result_modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[contains(@class,'modal')][.//*[contains(text(),'UPDATE RESULT') or contains(text(),'Update Result')]]"
            ))
        )
        success_td = result_modal.find_element(
            By.XPATH, ".//td[contains(text(),'Process completed successfully')]"
        )
        assert success_td.is_displayed()

    def test_c70556_view_history_billing_and_reversals_tabs(self, driver):
        """C70556 View History - Billing tab and Reversals tab."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 10)

        page.open_service_info_view_history()
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "#HistoryMapPopupContainer, #divCustomerServiceChangeHistory"
        )))

        # Click Billing tab
        tab_container = driver.find_element(By.ID, "parentTabContainerHistory")
        billing_link = tab_container.find_element(By.XPATH, ".//a[contains(text(),'Billing')]")
        assert billing_link.is_displayed()
        driver.execute_script("arguments[0].click();", billing_link)

        # Validate Billing tab is active
        billing_tab = WebDriverWait(driver, 8).until(
            lambda d: d.find_element(By.ID, "parentTabContainerHistory_3")
        )
        assert "active" in billing_tab.get_attribute("class")

        # Validate invoice table headers
        invoice_table = wait.until(
            EC.visibility_of_element_located((By.ID, "ServiceInvoiceDetailTable"))
        )
        popup = driver.find_element(By.ID, "HistoryMapPopupContainer")
        headers = popup.find_elements(By.CSS_SELECTOR, "#ServiceInvoiceDetailTable thead th")
        header_texts = [h.text for h in headers]
        for expected in ["InvoiceID", "Invoice Date", "Invoice Type", "Charge Code",
                         "Charge Type", "Dates", "Qty", "Amount", "Tax", "Total"]:
            assert any(expected in ht for ht in header_texts), (
                f"Header '{expected}' not found in billing table"
            )

        # Validate Display Zero Amounts checkbox exists and toggles
        chk = driver.find_element(By.ID, "chkActive")
        chk_label = chk.find_element(By.XPATH, "./ancestor::label")
        assert chk_label.is_displayed()
        was_checked = chk.is_selected()
        driver.execute_script("arguments[0].click();", chk)
        if was_checked:
            assert not chk.is_selected()
        else:
            assert chk.is_selected()
        driver.execute_script("arguments[0].click();", chk)
        if was_checked:
            assert chk.is_selected()
        else:
            assert not chk.is_selected()

        # Validate Types dropdown - open and select options
        types_btn = popup.find_element(
            By.XPATH, ".//button[contains(@class,'multiselect') and contains(@class,'dropdown-toggle') and contains(text(),'Types')]"
        )
        driver.execute_script("arguments[0].click();", types_btn)

        # Select Rental (4), Service (1), Surcharge (3)
        dropdown_menus = driver.find_elements(
            By.CSS_SELECTOR, "ul.multiselect-container.dropdown-menu"
        )
        visible_menu = None
        for menu in dropdown_menus:
            if menu.is_displayed():
                visible_menu = menu
                break
        assert visible_menu is not None, "Types dropdown menu should be visible"

        for val in ["4", "1", "3"]:
            cb = visible_menu.find_element(
                By.CSS_SELECTOR, f'input[type="checkbox"][value="{val}"]'
            )
            driver.execute_script("arguments[0].click();", cb)

        # Close dropdown by clicking elsewhere
        driver.execute_script("document.elementFromPoint(0, 0).click();")

        # Click Load button
        load_btn = popup.find_element(
            By.CSS_SELECTOR, 'a.btn.btn-primary[onclick*="GetBillingAuditOrderDetail"]'
        )
        assert load_btn.is_displayed()
        assert "Load" in load_btn.text
        driver.execute_script("arguments[0].click();", load_btn)

        # Update Bill Through Date
        update_btt_link = popup.find_element(
            By.CSS_SELECTOR,
            'a.btn.btn-primary.small_anchor_btn[onclick*="DisplayServiceBillingThroughDate"]'
        )
        assert update_btt_link.is_displayed()
        assert "Update Bill Through Date" in update_btt_link.text
        driver.execute_script("arguments[0].click();", update_btt_link)

        # Validate Bill Through Date modal
        btt_modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "modalServiceBillingThroughDate"))
        )
        modal_title = btt_modal.find_element(By.CSS_SELECTOR, ".modal-title")
        assert "Update Bill Through Date" in modal_title.text

        svc_id_span = btt_modal.find_element(By.ID, "spanBillingServiceIDDash")
        assert svc_id_span.text.strip() != ""

        assert btt_modal.find_element(By.ID, "txtServiceBillingThroughDate") is not None
        assert btt_modal.find_element(By.ID, "billingThroughtUpdatebox").is_displayed()

        # Click Update
        update_btn = btt_modal.find_element(By.ID, "btnBillingThroughDate")
        assert "Update" in update_btn.text
        driver.execute_script("arguments[0].click();", update_btn)

        # Click Close in the modal
        close_in_modal = btt_modal.find_element(By.ID, "btnServicePopupClose")
        assert "Close" in close_in_modal.text
        driver.execute_script("arguments[0].click();", close_in_modal)

        # Reversals tab
        reversals_link = tab_container.find_element(By.XPATH, ".//a[contains(text(),'Reversals')]")
        assert reversals_link.is_displayed()
        driver.execute_script("arguments[0].click();", reversals_link)

        reversals_tab = WebDriverWait(driver, 8).until(
            lambda d: d.find_element(By.ID, "parentTabContainerHistory_4")
        )
        assert "active" in reversals_tab.get_attribute("class")

        # Validate reversals table headers
        reversals_table = wait.until(
            EC.visibility_of_element_located((By.ID, "ServiceInfodeleteTable"))
        )
        rev_headers = popup.find_elements(By.CSS_SELECTOR, "#ServiceInfodeleteTable thead th")
        rev_header_texts = [h.text for h in rev_headers]
        for expected in [
            "Date", "User", "Change Reason", "Requested By", "End Date", "Start Date",
            "Frequency", "Status", "Qty", "Rate", "Prorate", "Rent Rate", "Rent Code",
            "PO", "Number", "Delete User"
        ]:
            assert any(expected in ht for ht in rev_header_texts), (
                f"Header '{expected}' not found in reversals table"
            )

        # Close View History popup
        common_popup = driver.find_element(By.ID, "commonHistoryMapPopup")
        close_popup = common_popup.find_element(By.ID, "btnServicePopupClose")
        driver.execute_script("arguments[0].click();", close_popup)
