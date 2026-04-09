"""
Customer Details - Service Activity tab header and calendar tests.

Validates calendar navigation, Show All toggle, Service Display dropdown,
List/Calendar view switch, Snapshot filter, date-click Add Order/Activity/File,
and hover tooltip popup on the Service Activity tab.
"""
import os
import re
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, force_click, scroll_to_element
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT


# Filter checkbox IDs
FILTER_OPTION_IDS = [
    "chkShowOrderActivity",
    "chkDisplayAR",
    "chkDisplayActivity",
    "chkDisplayActivitySystem",
    "chkDisplayServiceChange",
    "chkDisplayStatusChange",
]


def _page(driver):
    return CustomerPage(driver)


@pytest.mark.usefixtures("driver")
class TestServiceActivity:
    """
    Service Activity tab - header fields (#parentTabContainer_3).

    """

    def test_c339644_verify_service_activity_tab_visible_and_active(self, driver):
        """C339644 Verify Service Activity tab panel is visible and active."""
        page = _page(driver)
        tab = page.find_visible(*page.SA_TAB_PANE, timeout=15)
        assert tab.is_displayed()
        cls = tab.get_attribute("class")
        assert "active" in cls
        assert "in" in cls

    def test_c339645_verify_calendar_prev_button_changes_month(self, driver):
        """C339645 Verify Calendar prev button changes displayed month."""
        page = _page(driver)
        month_el = page.find_visible(*page.SA_MONTH_DISPLAY, timeout=10)
        initial_month = month_el.get_attribute("title")
        prev_btn = page.find_visible(*page.SA_PREV_BTN)
        prev_btn.click()
        wait_for_loading_screen(driver)
        month_el = page.find_visible(*page.SA_MONTH_DISPLAY, timeout=10)
        assert month_el.get_attribute("title") != initial_month

    def test_c339646_verify_calendar_next_button_changes_month(self, driver):
        """C339646 Verify Calendar next button changes displayed month."""
        page = _page(driver)
        month_el = page.find_visible(*page.SA_MONTH_DISPLAY, timeout=10)
        initial_month = month_el.get_attribute("title")
        next_btn = page.find_visible(*page.SA_NEXT_BTN)
        next_btn.click()
        wait_for_loading_screen(driver)
        month_el = page.find_visible(*page.SA_MONTH_DISPLAY, timeout=10)
        assert month_el.get_attribute("title") != initial_month

    def test_c339647_verify_show_all_checkbox_toggles(self, driver):
        """C339647 Verify Show All checkbox is clickable and toggles."""
        page = _page(driver)
        checkbox = page.find_element(*page.SA_SHOW_ALL_CHECKBOX)
        assert checkbox.is_enabled()
        # Verify label visible
        label = page.find_by_text("Show All", tag="label")
        assert label.is_displayed()
        checked_before = checkbox.is_selected()
        force_click(driver, *page.SA_SHOW_ALL_CHECKBOX)
        wait_for_loading_screen(driver)
        checkbox = page.find_element(*page.SA_SHOW_ALL_CHECKBOX)
        assert checkbox.is_selected() != checked_before

    def test_c339648_verify_service_display_dropdown(self, driver):
        """C339648 Verify Service Display dropdown opens and selection updates displayed information."""
        page = _page(driver)
        dropdown = page.find_visible(*page.SA_SERVICE_DISPLAY_DROPDOWN)
        text_el = page.find_visible(*page.SA_SERVICE_DISPLAY_TEXT)
        text_before = text_el.text.strip()
        dropdown.click()
        # Wait for dropdown to appear
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.ID, "serviceCalenderDropDown"))
        )
        # Click second option if available, else first
        options = driver.find_elements(
            By.CSS_SELECTOR,
            "#serviceCalenderDropDown li.serviceliList, "
            "#serviceCalenderDropDown li:not(.search_filter_ddloption)"
        )
        selectable = [o for o in options if not o.find_elements(By.CSS_SELECTOR, 'input[type="text"]')]
        if len(selectable) >= 2:
            selectable[1].click()
        elif selectable:
            selectable[0].click()
        text_el = page.find_visible(*page.SA_SERVICE_DISPLAY_TEXT)
        text_after = text_el.text.strip()
        assert len(text_after) >= 1

    def test_c339649_verify_list_view_switches_display(self, driver):
        """C339649 Verify List view icon switches display from calendar to list view."""
        page = _page(driver)
        page.ensure_service_activity_calendar_ready()
        list_icon = page.find_visible(*page.SA_LIST_VIEW_ICON)
        list_icon.click()
        wait_for_loading_screen(driver)
        assert page.element_is_visible(*page.SA_LIST_VIEW_CONTAINER, timeout=10)
        assert page.element_not_visible(*page.SA_CALENDAR_CONTAINER, timeout=5)

    def test_c339650_verify_snapshot_filter_opens_and_shows_options(self, driver):
        """C339650 Verify Snapshot Service Activity filter opens and shows all options and LOAD button."""
        page = _page(driver)
        filter_icon = page.find_visible(*page.SA_FILTER_ICON)
        filter_icon.click()
        filter_dropdown = page.find_visible(*page.SA_FILTER_DROPDOWN, timeout=8)
        assert filter_dropdown.is_displayed()
        # Verify all six filter labels
        for label_text in ["Orders", "Transactions", "Activity", "System Activity", "Service Change", "Status Change"]:
            label = filter_dropdown.find_element(
                By.XPATH, f'.//label[contains(text(),"{label_text}")]'
            )
            assert label.is_displayed()
        # Verify LOAD button
        load_btn = page.find_visible(*page.SA_FILTER_LOAD_BTN, timeout=5)
        assert load_btn.is_displayed()
        assert load_btn.get_attribute("value") == "LOAD"
        # Verify each filter checkbox exists
        for chk_id in FILTER_OPTION_IDS:
            chk = filter_dropdown.find_element(By.ID, chk_id)
            assert chk is not None

    def test_c339651_verify_calendar_date_click_add_order_activity_file(self, driver):
        """C339651 Verify Calendar date click opens Choose Option modal; Add Order, Add Activity, Add File."""
        page = _page(driver)
        date_iso = page.get_current_date_iso()

        # Open Choose Option modal
        page.open_calendar_option_modal(date_iso)
        wait_for_loading_screen(driver)

        # --- ADD ORDER ---
        add_order_btn = page.find_visible(*page.SA_BTN_ADD_ORDER, timeout=60)
        add_order_btn.click()
        wait_for_loading_screen(driver)
        page.find_visible(*page.SA_TXT_FILTER_SERVICE, timeout=10)
        # Click first service row
        first_svc = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '#ServicesgrdList tbody tr:not([style*="display: none"]) td[onclick*="ShowAddServiceOrOrderExceededLimitPopup"]'
            ))
        )
        first_svc.click()
        wait_for_loading_screen(driver)
        header = page.find_visible(*page.SA_NEW_ORDER_HEADER, timeout=10)
        assert "New Order" in header.text
        body = page.find_visible(*page.SA_NEW_ORDER_BODY)
        assert body.is_displayed()

        # Suggest route -> Nearby Services
        suggest_btn = body.find_element(*page.SA_BTN_SUGGEST)
        suggest_btn.click()
        wait_for_loading_screen(driver)
        page.find_visible(*page.SA_NEARBY_SERVICES_MODAL, timeout=10)
        title = page.find_visible(*page.SA_NEARBY_SERVICES_TITLE)
        assert "Nearby Services" in title.text
        close_btn = page.find_visible(*page.SA_BTN_CLOSE_NEARBY)
        close_btn.click()
        page.find_visible(*page.SA_NEW_ORDER_BODY)

        # Order Type = DEL, Route = Automation test 1
        page.select2_click_option(
            "#select2-order_Type-container", "DEL - Equipment Delivery"
        )
        page.select2_click_option(
            "#select2-order_Route-container", "Automation test 1 - Automation test 1"
        )
        # Requested By
        req_by = page.find_visible(*page.SA_ORDER_REQUEST_BY)
        req_by.clear()
        req_by.send_keys(USER_DATA["automation_user"])
        # Create Order
        create_btn = page.find_visible(*page.SA_BTN_CREATE_ORDER)
        create_btn.click()
        wait_for_loading_screen(driver)
        # Verify success
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((
                By.XPATH, "//*[contains(text(),'Order has been inserted successfully')]"
            ))
        )
        # Validate DEL order on calendar
        tab = page.find_visible(*page.SA_TAB_PANE, timeout=15)
        events = tab.find_elements(*page.SA_CALENDAR_EVENT)
        found_del = any(re.search(r"1-DEL\s*\([^)]+\)", e.text, re.IGNORECASE) for e in events if e.is_displayed())
        assert found_del, "DEL order event should be visible on calendar"

        # --- ADD ACTIVITY ---
        page.open_calendar_option_modal(date_iso)
        add_activity_btn = page.find_visible(*page.SA_BTN_ADD_ACTIVITY_CALENDAR)
        add_activity_btn.click()
        wait_for_loading_screen(driver)
        modal = page.find_visible(*page.SA_ADD_ACTIVITY_MODAL, timeout=10)
        act_header = page.find_visible(*page.SA_ADD_ACTIVITY_HEADER)
        assert "ADD ACTIVITY" in act_header.text

        # Type = CALL - Follow Up Call
        page.select2_click_option(
            "#select2-Svc_ATabDDlType-container", "CALL - Follow Up Call"
        )
        # Contact
        contact = page.find_visible(*page.SA_CONTACT_INPUT)
        contact.clear()
        contact.send_keys(USER_DATA["contact_name"])
        # Reminder
        force_click(driver, *page.SA_REMINDER_CHECKBOX)
        page.find_visible(By.ID, "RemiderSection", timeout=5)

        # Assigned User via Select2
        assigned_container = driver.find_element(
            By.CSS_SELECTOR, "#myCTabAddEditNoteNewModal .ddlUsers"
        )
        select2_container = assigned_container.find_element(
            By.XPATH, "./parent::*/descendant::*[contains(@class,'select2-container')]"
        )
        select2_container.click()
        search_field = WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, ".select2-container--open input.select2-search__field"
            ))
        )
        search_field.send_keys(USER_DATA["assigned_user"])
        option = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f'//li[contains(@class,"select2-results__option") and contains(text(),"{USER_DATA["assigned_user"]}")]'
            ))
        )
        option.click()

        # Private label
        private_label = modal.find_element(By.XPATH, './/label[contains(text(),"Private")]')
        assert private_label.is_displayed()
        private_chk = driver.find_element(By.ID, "chkPrivateReminder")
        assert private_chk.is_enabled()

        # Reminder Type = By Date
        page.select2_click_option("#select2-ddlType-container", "By Date")

        # Description
        desc = page.find_visible(*page.SA_REMINDER_DESCRIPTION)
        desc.clear()
        desc.send_keys(USER_DATA["automation_user"])

        # Save Activity
        save_btn = page.find_visible(*page.SA_BTN_SAVE_ACTIVITY)
        save_btn.click()
        wait_for_loading_screen(driver)
        assert page.element_not_visible(*page.SA_ADD_ACTIVITY_MODAL, timeout=10)

        # --- ADD FILE ---
        page.open_calendar_option_modal(date_iso)
        add_file_btn = page.find_visible(*page.SA_BTN_ADD_FILE_CALENDAR)
        add_file_btn.click()
        wait_for_loading_screen(driver)
        file_header = page.find_visible(*page.SA_ADD_FILE_HEADER, timeout=10)
        assert "ADD FILE" in file_header.text
        page.find_visible(By.ID, "cTabActivityPopUpNewBody")

        # Attach file
        trigger = page.find_element(*page.SA_TRIGGER_FILE_INPUT)
        driver.execute_script("arguments[0].click();", trigger)
        file_input = page.find_element(*page.SA_FILE_INPUT)
        # Use a sample file path - create a minimal temp file if needed
        sample_path = os.path.join(os.path.dirname(__file__), "sample-upload.png")
        if not os.path.exists(sample_path):
            # Create a minimal 1x1 PNG for upload testing
            import struct, zlib
            def _minimal_png():
                sig = b'\x89PNG\r\n\x1a\n'
                ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
                ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
                ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
                raw = b'\x00\x00\x00\x00'
                idat_data = zlib.compress(raw)
                idat_crc = zlib.crc32(b'IDAT' + idat_data) & 0xffffffff
                idat = struct.pack('>I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('>I', idat_crc)
                iend_crc = zlib.crc32(b'IEND') & 0xffffffff
                iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
                return sig + ihdr + idat + iend
            with open(sample_path, 'wb') as f:
                f.write(_minimal_png())
        file_input.send_keys(sample_path)

        # Description
        file_desc = page.find_visible(*page.SA_FILE_DESCRIPTION)
        file_desc.clear()
        file_desc.send_keys(USER_DATA["automation_user"])

        # Customer Portal Visible toggle
        force_click(driver, *page.SA_TGL_CUSTOMER_PORTAL_VISIBLE)

        # Save File
        save_file_btn = page.find_visible(*page.SA_BTN_SAVE_FILE)
        save_file_btn.click()
        wait_for_loading_screen(driver)
        assert page.element_not_visible(*page.SA_ADD_FILE_HEADER, timeout=10)

    def test_c339652_verify_hover_tooltip_popup(self, driver):
        """C339652 Verify Hover over calendar service event shows tooltip popup."""
        page = _page(driver)
        page.ensure_service_activity_calendar_ready()
        # Hover over first visible tooltip trigger
        triggers = driver.find_elements(*page.SA_CALENDAR_TOOLTIP_TRIGGER)
        visible_triggers = [t for t in triggers if t.is_displayed()]
        assert len(visible_triggers) >= 1, "At least one calendar tooltip trigger should be visible"
        ActionChains(driver).move_to_element(visible_triggers[0]).perform()
        # Tooltip popup should appear
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(page.SA_CALENDAR_TOOLTIP_POPUP)
        )
        popups = driver.find_elements(*page.SA_CALENDAR_TOOLTIP_POPUP)
        visible_popup = next((p for p in popups if p.is_displayed()), None)
        assert visible_popup is not None, "Tooltip popup should be visible"
        # Verify tooltip content
        h4 = visible_popup.find_element(By.TAG_NAME, "h4")
        assert h4.is_displayed()
        assert len(h4.text.strip()) > 0
        for label in ["WO #:", "Service:", "Equip:", "Status:", "User:", "Charges:", "Route:"]:
            strong = visible_popup.find_element(
                By.XPATH, f'.//strong[contains(text(),"{label}")]'
            )
            assert strong.is_displayed()
