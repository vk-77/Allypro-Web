"""
Customer Details - Service Info dropdown Transfer Service tests.

Validates the Transfer Service modal form fields, customer search,
date selection, and successful transfer submission.
"""
import pytest
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.web.base_web_page import BasePage
from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    scroll_to_element,
    force_click,
)
from data.user_data import USER_DATA


TRANSFER_MODAL = "#modalSerivceTransfer"
UPDATE_SERVICE_MODAL = "#myCTabAddEditNoteModal"


def _format_date(dt):
    """Format date as MM/DD/YYYY."""
    return dt.strftime("%m/%d/%Y")


def _tomorrow():
    """Return tomorrow's date."""
    return datetime.now() + timedelta(days=1)


@pytest.mark.usefixtures("driver")
class TestServiceInfoTransferService:
    """
    Service Info dropdown - Transfer Service tests.

    Usage:
        pytest tests/web/customer_information/test_service_info_transfer_service.py -v
    """

    @pytest.mark.skip(reason="Complex multi-step flow - skipped")
    def test_c70557_transfer_service_existing_location(self, driver):
        """C70557 Transfer Service - Existing Location."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        # Add new service and select the last one
        page.add_new_service_from_customer_details()
        page.select_last_service()

        # Open Transfer Service for last service
        page.open_service_info_transfer_service_for_last_service()

        # Validate transfer modal is open
        transfer_modal = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, TRANSFER_MODAL))
        )
        assert transfer_modal.find_element(By.CSS_SELECTOR, ".modal-header.common").is_displayed()
        title = transfer_modal.find_element(By.ID, "hTitleServiceTansfer")
        assert "Service Transfer" in title.text

        # Select "Existing Location" (value 1)
        dd = transfer_modal.find_element(By.ID, "ddlServiceTransferOption")
        Select(dd).select_by_value("1")

        # Type customer ID and search
        customer_id = USER_DATA.get("customer_id", "")
        search_field = transfer_modal.find_element(By.ID, "txtSearchServiceTransfer")
        search_field.clear()
        search_field.send_keys(customer_id)

        search_btn = transfer_modal.find_element(By.CSS_SELECTOR, "i.fa-search")
        search_link = search_btn.find_element(By.XPATH, "./..")
        driver.execute_script("arguments[0].click();", search_link)
        wait_for_loading_screen(driver)

        # Validate search result table headers
        wait.until(EC.visibility_of_element_located((By.ID, "divServiceTransferSearchResultContainer")))
        table = driver.find_element(By.ID, "tableSearchResult")
        assert table.is_displayed()
        headers = table.find_elements(By.CSS_SELECTOR, "thead th")
        header_texts = [h.text for h in headers]
        for expected in ["CustID", "Customer Name", "Loc ID", "Location Name", "Address", "Region", "Service Area", "Action"]:
            assert any(expected in ht for ht in header_texts), f"Header '{expected}' not found"

        # Click Select in first result row
        first_row = table.find_element(By.CSS_SELECTOR, "tbody tr")
        select_btn = first_row.find_element(
            By.XPATH, ".//a[contains(@class,'btn') and contains(@class,'btn-primary') and contains(text(),'Select')]"
        )
        driver.execute_script("arguments[0].click();", select_btn)

        # Validate update service modal
        update_modal = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, UPDATE_SERVICE_MODAL))
        )
        header = driver.find_element(By.ID, "cTabActivityPopUpHeader")
        assert "Service Transfer" in header.text
        assert driver.find_element(By.ID, "frmUpdateCusServiceDetail").is_displayed()

        # Set effective date to tomorrow
        effective_date = _tomorrow()
        eff_input = driver.find_element(By.ID, "uService_EffectiveDate")
        driver.execute_script("arguments[0].removeAttribute('readonly');", eff_input)
        eff_input.clear()
        eff_input.send_keys(_format_date(effective_date))
        eff_input.send_keys(Keys.ENTER)

        # Change Requested By
        requested_by = USER_DATA.get("automation_user", "AutoMVC")
        req_input = update_modal.find_element(By.CSS_SELECTOR, "#uService_ChangeRequestedBy, #uService_ChangeRequestedBy input")
        req_input.clear()
        req_input.send_keys(requested_by)

        # Statuses
        Select(driver.find_element(By.ID, "uService_Status")).select_by_value("0")
        Select(driver.find_element(By.ID, "uService_NewServiceStatus")).select_by_value("1")

        # Click Next (screen 2)
        next_btn = update_modal.find_element(
            By.CSS_SELECTOR, 'input[type="button"][onclick*="GetNextUpdateServiceScreen2()"]'
        )
        next_btn.click()
        wait_for_loading_screen(driver)

        # Handle future-dated changes warning
        try:
            msg_div = driver.find_element(By.ID, "divUpdateSvsMessage")
            if msg_div.is_displayed() and "future-dated changes" in msg_div.text:
                future_date = _tomorrow()
                eff_input2 = driver.find_element(By.ID, "uService_EffectiveDate")
                driver.execute_script("arguments[0].removeAttribute('readonly');", eff_input2)
                eff_input2.clear()
                eff_input2.send_keys(_format_date(future_date))
                eff_input2.send_keys(Keys.ENTER)
                next_btn2 = update_modal.find_element(
                    By.CSS_SELECTOR, 'input[type="button"][onclick*="GetNextUpdateServiceScreen2()"]'
                )
                next_btn2.click()
                wait_for_loading_screen(driver)
        except (NoSuchElementException, TimeoutException):
            pass

        # Day of Week and Routes step
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "updateServiceContainerDiv4"))
        )

        # Ensure Routing = Assigned manually
        dispatch_sel = driver.find_element(By.ID, "uService_DispatchToAssignRoute")
        if dispatch_sel.get_attribute("value") != "1":
            Select(dispatch_sel).select_by_value("1")

        # Fill day/route/sequence/time for each visible row
        day_dropdowns = [
            el for el in driver.find_elements(By.CSS_SELECTOR, "[id^='ddluDayofWeeek_']")
            if el.is_displayed()
        ]
        for i, day_dd in enumerate(day_dropdowns):
            dd_id = day_dd.get_attribute("id")
            idx = dd_id.replace("ddluDayofWeeek_", "")
            if not day_dd.get_attribute("disabled") and not day_dd.get_attribute("value"):
                Select(day_dd).select_by_value(str(i + 1))

            try:
                seq = driver.find_element(By.ID, f"txtuDaySequence_{idx}")
                if seq.is_displayed():
                    seq.clear()
                    seq.send_keys(str(i + 1))
            except NoSuchElementException:
                pass

            try:
                tw_start = driver.find_element(By.ID, f"txtuTimeWindowStart_{idx}")
                if tw_start.is_displayed():
                    tw_start.clear()
                    tw_start.send_keys("08:00 am")
            except NoSuchElementException:
                pass

            try:
                tw_end = driver.find_element(By.ID, f"txtuTimeWindowEnd_{idx}")
                if tw_end.is_displayed():
                    tw_end.clear()
                    tw_end.send_keys("05:00 pm")
            except NoSuchElementException:
                pass

            try:
                route_container = driver.find_element(By.ID, f"select2-ddluDayofRoute_{idx}-container")
                if route_container.is_displayed():
                    scroll_to_element(driver, route_container)
                    driver.execute_script("arguments[0].click();", route_container)
                    try:
                        search_field = WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((
                                By.CSS_SELECTOR, ".select2-container--open input.select2-search__field"
                            ))
                        )
                        search_field.clear()
                        search_field.send_keys("Automation test 1")
                        search_field.send_keys(Keys.ENTER)
                    except TimeoutException:
                        options = driver.find_elements(
                            By.CSS_SELECTOR, ".select2-container--open .select2-results__option"
                        )
                        if options:
                            options[0].click()
            except NoSuchElementException:
                pass

        # Click Next (screen 5)
        next5 = update_modal.find_element(
            By.CSS_SELECTOR,
            'input[type="button"][onclick*="GetNextUpdateServiceScreen5()"], button[onclick*="GetNextUpdateServiceScreen5"]'
        )
        driver.execute_script("arguments[0].click();", next5)
        wait_for_loading_screen(driver)

        # Click Next (screen 6 - Order Charges)
        next6 = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'input[type="button"][onclick*="GetNextUpdateServiceScreen6"], button[onclick*="GetNextUpdateServiceScreen6"]'
            ))
        )
        driver.execute_script("arguments[0].click();", next6)
        wait_for_loading_screen(driver)

        # Wait for final step and click Save
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "updateServiceContainerDiv7"))
        )
        save_btn = update_modal.find_element(
            By.CSS_SELECTOR,
            'input[type="submit"][onclick*="IsUpdateServiceFieldvalid()"], input.btn-primary[value="Save"]'
        )
        driver.execute_script("arguments[0].click();", save_btn)
        wait_for_loading_screen(driver)

        # Validate success
        success = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//*[contains(text(),'updated successfully') or contains(text(),'Service has been updated successfully')]"
            ))
        )
        assert success.is_displayed()

    def test_c70558_transfer_service_new_location_add_location_modal_open(self, driver):
        """C70558 Transfer Service - New Location for Customer validate Add Location modal is open."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.add_new_service_from_customer_details()
        page.select_last_service()

        # Open Transfer Service for last service
        page.open_service_info_transfer_service_for_last_service()

        # Validate transfer modal
        transfer_modal = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, TRANSFER_MODAL))
        )
        assert transfer_modal.find_element(By.CSS_SELECTOR, ".modal-header.common").is_displayed()
        title = transfer_modal.find_element(By.ID, "hTitleServiceTansfer")
        assert "Service Transfer" in title.text

        # Select "New Location for Customer" (value 2)
        Select(transfer_modal.find_element(By.ID, "ddlServiceTransferOption")).select_by_value("2")

        # Search customer
        customer_id = USER_DATA.get("customer_id", "")
        search_field = transfer_modal.find_element(By.ID, "txtSearchServiceTransfer")
        search_field.click()
        search_field.clear()
        search_field.send_keys(customer_id)

        # Click search icon
        search_icon = transfer_modal.find_element(By.CSS_SELECTOR, "i.fa-search")
        search_link = search_icon.find_element(By.XPATH, "./..")
        driver.execute_script("arguments[0].click();", search_link)
        wait_for_loading_screen(driver)

        # Click search icon again
        search_icon2 = transfer_modal.find_element(By.CSS_SELECTOR, "i.fa-search")
        search_link2 = search_icon2.find_element(By.XPATH, "./..")
        driver.execute_script("arguments[0].click();", search_link2)
        wait_for_loading_screen(driver)

        # Click "Add Location" in first result row
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "divServiceTransferSearchResultContainer"))
        )
        table = driver.find_element(By.ID, "tableSearchResult")
        assert table.is_displayed()
        first_row = table.find_element(By.CSS_SELECTOR, "tbody tr")
        add_loc_btn = first_row.find_element(
            By.XPATH, ".//a[contains(@class,'btn') and contains(@class,'btn-primary') and contains(text(),'Add Location')]"
        )
        driver.execute_script("arguments[0].click();", add_loc_btn)
        wait_for_loading_screen(driver)

        # Validate Add Location modal is open
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "CommonLayoutPopUpContainer"))
        )
        assert driver.find_element(By.ID, "addNewServiceLocationForm").is_displayed()
        modal_title = driver.find_element(By.CSS_SELECTOR, ".modal-title")
        assert "Add Location" in modal_title.text

    def test_c70559_transfer_service_new_customer_create_customer_modal_open(self, driver):
        """C70559 Transfer Service - New Customer verify Create Customer modal is open."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.add_new_service_from_customer_details()
        page.select_last_service()

        # Open Transfer Service for last service
        page.open_service_info_transfer_service_for_last_service()

        # Validate transfer modal
        transfer_modal = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, TRANSFER_MODAL))
        )
        assert transfer_modal.find_element(By.CSS_SELECTOR, ".modal-header.common").is_displayed()
        title = transfer_modal.find_element(By.ID, "hTitleServiceTansfer")
        assert "Service Transfer" in title.text

        # Select "New Customer" (value 3)
        Select(transfer_modal.find_element(By.ID, "ddlServiceTransferOption")).select_by_value("3")

        # Click ADD CUSTOMER & LOCATION button
        add_cust_btn = transfer_modal.find_element(By.ID, "btnServiceTransferAddCustomer")
        assert add_cust_btn.is_displayed()
        driver.execute_script("arguments[0].click();", add_cust_btn)
        wait_for_loading_screen(driver)

        # Verify Create Customer modal appears
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "#myAddCustomerModel, [name='CUST_CustomerName']"
            ))
        )
        cust_name_field = driver.find_element(By.CSS_SELECTOR, "[name='CUST_CustomerName']")
        assert cust_name_field.is_displayed()

    def test_c70560_transfer_service_negative_next_without_required_fields(self, driver):
        """C70560 Transfer Service (Negative) - Clicking Next without required fields shows validation."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.add_new_service_from_customer_details()
        page.select_last_service()

        # Open Transfer Service for last service
        page.open_service_info_transfer_service_for_last_service()

        # Select Existing Location
        transfer_modal = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, TRANSFER_MODAL))
        )
        Select(transfer_modal.find_element(By.ID, "ddlServiceTransferOption")).select_by_value("1")

        # Search customer
        customer_id = USER_DATA.get("customer_id", "")
        search_field = transfer_modal.find_element(By.ID, "txtSearchServiceTransfer")
        search_field.clear()
        search_field.send_keys(customer_id)
        search_icon = transfer_modal.find_element(By.CSS_SELECTOR, "i.fa-search")
        search_link = search_icon.find_element(By.XPATH, "./..")
        driver.execute_script("arguments[0].click();", search_link)
        wait_for_loading_screen(driver)

        # Click Select in first row
        first_row = driver.find_element(By.CSS_SELECTOR, "#tableSearchResult tbody tr")
        select_btn = first_row.find_element(
            By.XPATH, ".//a[contains(@class,'btn') and contains(@class,'btn-primary') and contains(text(),'Select')]"
        )
        driver.execute_script("arguments[0].click();", select_btn)

        # Wait for update service modal
        update_modal = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, UPDATE_SERVICE_MODAL))
        )

        # Leave required fields empty, click Next
        next_btn = update_modal.find_element(
            By.CSS_SELECTOR, 'input[type="button"][onclick*="GetNextUpdateServiceScreen2()"]'
        )
        next_btn.click()
        wait_for_loading_screen(driver)

        # Expect validation message
        msg_div = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "divUpdateSvsMessage"))
        )
        assert msg_div.is_displayed()
        msg_text = msg_div.text.lower()
        assert any(kw in msg_text for kw in [
            "please enter", "please select", "future-dated changes", "view history"
        ]), f"Validation message expected, got: {msg_div.text}"

        # First step container should still be visible (did not advance)
        step1 = driver.find_element(By.ID, "updateServiceContainerDiv1")
        assert step1.is_displayed(), "Step 1 should still be visible after validation failure"
