"""
Customer Details - Account Activity toolbar actions tests.

"""
import os
import pytest
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select_option,
    scroll_to_element,
    force_click,
)
from data.user_data import USER_DATA


ACCOUNT_ACTIVITY_CONTAINER = "#parentTabContainer_4"
ADD_EDIT_MODAL = "#myCTabAddEditNoteNewModal"
MODAL_HEADER = "#cTabActivityPopUpNewHeader"


@pytest.mark.usefixtures("driver")
class TestAccountActivityActions:
    """Account Activity toolbar action tests (#parentTabContainer_4).

    Usage:
        pytest tests/web/test_01_5_customer_detail_account_activity/test_actions.py -v
    """

    # ------------------------------------------------------------------
    # C346265 - Add Activity
    # ------------------------------------------------------------------
    def test_c346265_add_activity_opens_panel_fills_and_saves(self, driver):
        """C346265 Add Activity opens panel, fills Type Contact reminder user By Date description and saves."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        # Click "Add Activity" button inside the Account Activity container
        add_activity_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, f'{ACCOUNT_ACTIVITY_CONTAINER} a[title="Add Activity"]'
        )))
        add_activity_btn.click()
        wait_for_loading_screen(driver)

        # Modal should be visible with header "ADD ACTIVITY"
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ADD_EDIT_MODAL)))
        header = driver.find_element(By.CSS_SELECTOR, MODAL_HEADER)
        assert "ADD ACTIVITY" in header.text

        # Select Type: "CALL - Follow Up Call" via Select2
        driver.find_element(By.CSS_SELECTOR, "#select2-Svc_ATabDDlType-container").click()
        call_option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//li[contains(@class,'select2-results__option') and contains(text(),'CALL - Follow Up Call')]"
        )))
        call_option.click()

        # Fill Contact field
        contact_field = wait.until(EC.visibility_of_element_located((By.ID, "Svc_ATabContact")))
        contact_field.clear()
        contact_field.send_keys(USER_DATA["automation_user"])

        # Check Reminder checkbox
        reminder_cb = driver.find_element(By.ID, "Reminder")
        driver.execute_script("arguments[0].click();", reminder_cb)

        # Wait for reminder section to appear
        wait.until(EC.visibility_of_element_located((By.ID, "RemiderSection")))

        # Select assigned user in the reminder user dropdown (Select2 inside modal)
        modal = driver.find_element(By.CSS_SELECTOR, ADD_EDIT_MODAL)
        ddl_users_parent = modal.find_element(By.CSS_SELECTOR, ".ddlUsers")
        select2_container = ddl_users_parent.find_element(
            By.XPATH, "./parent::*"
        ).find_element(By.CSS_SELECTOR, ".select2-container")
        select2_container.click()

        search_field = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, ".select2-container--open input.select2-search__field"
        )))
        search_field.send_keys(USER_DATA["assigned_user"])
        user_option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//li[contains(@class,'select2-results__option') and contains(text(),'{USER_DATA['assigned_user']}')]"
        )))
        user_option.click()

        # Select reminder type "By Date"
        driver.find_element(By.CSS_SELECTOR, "#select2-ddlType-container").click()
        by_date_option = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//li[contains(@class,'select2-results__option') and contains(text(),'By Date')]"
        )))
        by_date_option.click()

        # Fill Description
        desc_field = wait.until(EC.visibility_of_element_located((By.ID, "Description")))
        desc_field.clear()
        desc_field.send_keys(USER_DATA["automation_user"])

        # Click Save
        save_btn = modal.find_element(By.CSS_SELECTOR, 'input[onclick="AddTabNotesDetail()"]')
        save_btn.click()
        wait_for_loading_screen(driver)

        # Modal should close
        assert page.element_not_visible(By.CSS_SELECTOR, ADD_EDIT_MODAL)

    # ------------------------------------------------------------------
    # C346266 - Add File
    # ------------------------------------------------------------------
    def test_c346266_add_file_opens_panel_uploads_and_saves(self, driver):
        """C346266 Add File opens panel, add-more and delete rows, uploads file, level description portal toggle and saves."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        # Click "Add File" button
        add_file_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, f'{ACCOUNT_ACTIVITY_CONTAINER} a[title="Add File"]'
        )))
        add_file_btn.click()
        wait_for_loading_screen(driver)

        # Modal visible with header "ADD FILE"
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ADD_EDIT_MODAL)))
        header = driver.find_element(By.CSS_SELECTOR, MODAL_HEADER)
        assert "ADD FILE" in header.text

        # Verify tab popup ID contains "2"
        tab_id = driver.find_element(By.ID, "spnTabpopUpID")
        assert "2" in tab_id.text

        # Add more rows and delete them
        modal = driver.find_element(By.CSS_SELECTOR, ADD_EDIT_MODAL)
        modal.find_element(By.ID, "btnMore_1").click()
        wait.until(EC.presence_of_element_located((By.ID, "divCon_2")))

        modal.find_element(By.ID, "btnMore_1").click()
        wait.until(EC.presence_of_element_located((By.ID, "divCon_3")))

        # Delete row 3
        modal.find_element(By.ID, "btnMore_3").click()
        WebDriverWait(driver, 5).until(
            EC.staleness_of(driver.find_element(By.ID, "divCon_3"))
            if page.element_exists(By.ID, "divCon_3", timeout=1) else lambda d: True
        )

        # Delete row 2
        modal.find_element(By.ID, "btnMore_2").click()
        WebDriverWait(driver, 5).until(
            lambda d: not page.element_exists(By.ID, "divCon_2", timeout=1)
        )

        # Upload file
        driver.find_element(By.ID, "triggerFileInput").click()
        file_input = driver.find_element(By.ID, "Svc_ATabNoteFile_1")
        upload_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            "data", "fixtures", "sample-upload.png"
        )
        # If the fixture file does not exist, use a fallback approach
        if not os.path.exists(upload_path):
            # Create a minimal PNG for the test
            fixtures_dir = os.path.dirname(upload_path)
            os.makedirs(fixtures_dir, exist_ok=True)
            # Minimal 1x1 PNG
            import base64
            png_data = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            )
            with open(upload_path, "wb") as f:
                f.write(png_data)
        file_input.send_keys(upload_path)

        # Verify file name shown
        file_name_el = wait.until(EC.visibility_of_element_located((By.ID, "divcTabActivityFileName_1")))
        assert "sample-upload.png" in file_name_el.text

        # Select file level = 1 (Service), verify service DDL visible
        level_select = Select(driver.find_element(By.ID, "Svc_ATabFileLevel"))
        level_select.select_by_value("1")
        assert driver.find_element(By.ID, "Svc_ATabFileLevel").get_attribute("value") == "1"
        assert page.element_is_visible(By.ID, "divSvcActivityServiceDDL")

        # Select file level = 0 (Customer), verify service DDL not visible
        level_select.select_by_value("0")
        assert driver.find_element(By.ID, "Svc_ATabFileLevel").get_attribute("value") == "0"
        assert page.element_not_visible(By.ID, "divSvcActivityServiceDDL")

        # Fill description
        desc_field = wait.until(EC.visibility_of_element_located((By.ID, "Svc_ATabFileDescription")))
        desc_field.clear()
        desc_field.send_keys(USER_DATA["automation_user"])

        # Toggle portal visibility checkbox
        portal_toggle = driver.find_element(By.ID, "tglAddFileCustomerPortalVisible")
        assert not portal_toggle.is_selected()
        driver.execute_script("arguments[0].click();", portal_toggle)
        assert portal_toggle.is_selected()

        # Click Save
        save_btn = modal.find_element(By.CSS_SELECTOR, 'input[onclick="AddFileTabNotesDetail()"]')
        save_btn.click()
        wait_for_loading_screen(driver)

        # Modal should close
        assert page.element_not_visible(By.CSS_SELECTOR, ADD_EDIT_MODAL)

    # ------------------------------------------------------------------
    # C346267 - Edit sets priority, saves, re-opens to verify persistence
    # ------------------------------------------------------------------
    def test_c346267_edit_sets_priority_high_saves_and_persists(self, driver):
        """C346267 Edit opens modal, sets Priority to High, saves, and persists on re-open."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        # Click first Edit button
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'{ACCOUNT_ACTIVITY_CONTAINER} tr.dx-data-row button[title="Edit"]'
        )))
        edit_btn.click()
        wait_for_loading_screen(driver)

        # Modal visible
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ADD_EDIT_MODAL)))

        # Set Priority to High (value=1)
        priority_select = wait.until(EC.visibility_of_element_located((By.ID, "ddlPriority")))
        Select(priority_select).select_by_value("1")
        assert priority_select.get_attribute("value") == "1"

        # Save
        modal = driver.find_element(By.CSS_SELECTOR, ADD_EDIT_MODAL)
        save_btn = modal.find_element(By.CSS_SELECTOR, 'input[onclick="AddTabNotesDetail()"]')
        save_btn.click()
        wait_for_loading_screen(driver)

        # Modal should close
        assert page.element_not_visible(By.CSS_SELECTOR, ADD_EDIT_MODAL)

        # Re-open the same record and verify priority persisted
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'{ACCOUNT_ACTIVITY_CONTAINER} tr.dx-data-row button[title="Edit"]'
        )))
        edit_btn.click()
        wait_for_loading_screen(driver)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ADD_EDIT_MODAL)))

        priority_select = driver.find_element(By.ID, "ddlPriority")
        assert priority_select.get_attribute("value") == "1"

        # Close modal
        modal = driver.find_element(By.CSS_SELECTOR, ADD_EDIT_MODAL)
        close_btn = modal.find_element(By.CSS_SELECTOR, "button.closeBtn")
        driver.execute_script("arguments[0].click();", close_btn)
        wait_for_loading_screen(driver)
        assert page.element_not_visible(By.CSS_SELECTOR, ADD_EDIT_MODAL)

    # ------------------------------------------------------------------
    # C346268 - Edit then Delete
    # ------------------------------------------------------------------
    def test_c346268_edit_delete_confirms_and_closes(self, driver):
        """C346268 Edit opens panel, Delete confirms via native dialog and closes panel."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        # Pre-accept the confirm dialog
        driver.execute_script("window.confirm = function() { return true; };")

        # Click first Edit button
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'{ACCOUNT_ACTIVITY_CONTAINER} tr.dx-data-row button[title="Edit"]'
        )))
        edit_btn.click()
        wait_for_loading_screen(driver)

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ADD_EDIT_MODAL)))

        # Click Delete button
        modal = driver.find_element(By.CSS_SELECTOR, ADD_EDIT_MODAL)
        delete_btn = modal.find_element(
            By.CSS_SELECTOR,
            'input[type="button"][onclick="DeleteTabActivityNotes()"][value="Delete"]'
        )
        delete_btn.click()
        wait_for_loading_screen(driver)

        # Modal should close
        assert page.element_not_visible(By.CSS_SELECTOR, ADD_EDIT_MODAL)

    # ------------------------------------------------------------------
    # C346269 - Pagination
    # ------------------------------------------------------------------
    def test_c346269_pagination_items_per_page_options(self, driver):
        """C346269 Pagination: items-per-page options are visible and selectable."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        pager = f"{ACCOUNT_ACTIVITY_CONTAINER} .dx-datagrid-pager"
        page_sizes = f"{pager} .dx-page-sizes"
        items_per_page_sizes = ["10", "20", "50", "100", "200", "250", "500"]

        # Scroll pager into view
        pager_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, pager)))
        scroll_to_element(driver, pager_el)

        page_sizes_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, page_sizes)))
        assert page_sizes_el.is_displayed()

        # Get current selection and click an alternate
        current_sel = driver.find_element(
            By.CSS_SELECTOR, f"{page_sizes} .dx-page-size.dx-selection"
        )
        current_label = current_sel.get_attribute("aria-label") or ""
        current_val = re.sub(r"^Items per page:\s*", "", current_label, flags=re.IGNORECASE).strip()
        others = [s for s in items_per_page_sizes if s != current_val]
        alternate = others[-1] if others else others[0]

        alt_btn = driver.find_element(
            By.CSS_SELECTOR,
            f'{page_sizes} [role="button"][aria-label="Items per page: {alternate}"]'
        )
        scroll_to_element(driver, alt_btn)
        driver.execute_script("arguments[0].click();", alt_btn)
        wait_for_loading_screen(driver)

        # Click each page size option and verify it becomes selected
        for size in items_per_page_sizes:
            size_btn = driver.find_element(
                By.CSS_SELECTOR,
                f'{page_sizes} [role="button"][aria-label="Items per page: {size}"]'
            )
            scroll_to_element(driver, size_btn)
            driver.execute_script("arguments[0].click();", size_btn)
            wait_for_loading_screen(driver)

            selected = driver.find_element(
                By.CSS_SELECTOR,
                f'{page_sizes} [aria-label="Items per page: {size}"]'
            )
            assert "dx-selection" in selected.get_attribute("class")

    # ------------------------------------------------------------------
    # C346270 - Create Filter
    # ------------------------------------------------------------------
    def test_c346270_create_filter_add_condition_activity_contains_customer(self, driver):
        """C346270 Create Filter: Add condition Activity contains Customer and verify filter panel."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)
        filter_value = "Customer"

        # Click "Create Filter" link inside the container
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        create_filter_link = container.find_element(
            By.XPATH, ".//*[contains(@class,'dx-datagrid-filter-panel-text') and contains(text(),'Create Filter')]"
        )
        scroll_to_element(driver, create_filter_link)
        create_filter_link.click()

        # Wait for Filter Builder dialog
        filter_builder = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class,'dx-overlay-wrapper')][.//text()[contains(.,'Filter Builder')]]"
        )))

        # Click Add button
        add_btn = filter_builder.find_element(
            By.CSS_SELECTOR, '[aria-label="Add"], .dx-filterbuilder-action-icon.dx-icon-plus'
        )
        add_btn.click()

        # Click "Add Condition"
        add_condition = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//li[@aria-label="Add Condition"]//*[contains(@class,"dx-treeview-item-content")] | //*[@aria-label="Add Condition"]//*[contains(@class,"dx-item-content")]'
        )))
        driver.execute_script("arguments[0].click();", add_condition)

        # Click value field and type filter value
        value_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            ".dx-filterbuilder-item-value-text"
        )))
        driver.execute_script("arguments[0].click();", value_field)

        # Type into the focused input
        active_el = driver.switch_to.active_element
        active_el.send_keys(filter_value)

        # Click OK
        ok_btn = filter_builder.find_element(
            By.XPATH, ".//div[contains(@class,'dx-button')]//span[contains(@class,'dx-button-text') and text()='OK']/ancestor::div[contains(@class,'dx-button')]"
        )
        ok_btn.click()
        wait_for_loading_screen(driver)

        # Verify filter panel shows Activity and the filter value
        filter_panel = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            f"{ACCOUNT_ACTIVITY_CONTAINER} .dx-datagrid-filter-panel"
        )))
        panel_text = filter_panel.text
        assert "Activity" in panel_text
        assert filter_value in panel_text

    # ------------------------------------------------------------------
    # C346271 - Clear filter
    # ------------------------------------------------------------------
    def test_c346271_clear_filter_removes_filter_builder_condition(self, driver):
        """C346271 Clear filter - panel Clear removes Filter Builder condition."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)
        filter_value = "Customer"

        # Create a filter first (same steps as C346270)
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        create_filter_link = container.find_element(
            By.XPATH, ".//*[contains(@class,'dx-datagrid-filter-panel-text') and contains(text(),'Create Filter')]"
        )
        scroll_to_element(driver, create_filter_link)
        create_filter_link.click()

        filter_builder = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class,'dx-overlay-wrapper')][.//text()[contains(.,'Filter Builder')]]"
        )))

        add_btn = filter_builder.find_element(
            By.CSS_SELECTOR, '[aria-label="Add"], .dx-filterbuilder-action-icon.dx-icon-plus'
        )
        add_btn.click()

        add_condition = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//li[@aria-label="Add Condition"]//*[contains(@class,"dx-treeview-item-content")] | //*[@aria-label="Add Condition"]//*[contains(@class,"dx-item-content")]'
        )))
        driver.execute_script("arguments[0].click();", add_condition)

        value_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, ".dx-filterbuilder-item-value-text"
        )))
        driver.execute_script("arguments[0].click();", value_field)
        active_el = driver.switch_to.active_element
        active_el.send_keys(filter_value)

        ok_btn = filter_builder.find_element(
            By.XPATH, ".//div[contains(@class,'dx-button')]//span[contains(@class,'dx-button-text') and text()='OK']/ancestor::div[contains(@class,'dx-button')]"
        )
        ok_btn.click()
        wait_for_loading_screen(driver)

        # Verify filter panel shows the value
        filter_panel = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            f"{ACCOUNT_ACTIVITY_CONTAINER} .dx-datagrid-filter-panel"
        )))
        assert filter_value in filter_panel.text

        # Click Clear
        clear_btn = container.find_element(
            By.CSS_SELECTOR, ".dx-datagrid-filter-panel-clear-filter"
        )
        assert clear_btn.is_displayed()
        assert "Clear" in clear_btn.text
        clear_btn.click()
        wait_for_loading_screen(driver)

        # Verify the filter condition text is gone
        panel_after = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            f"{ACCOUNT_ACTIVITY_CONTAINER} .dx-datagrid-filter-panel"
        )))
        assert not re.search(r"Contains\s+'Customer'", panel_after.text, re.IGNORECASE)

    # ------------------------------------------------------------------
    # C346272 - Field Selector / Column Chooser
    # ------------------------------------------------------------------
    def test_c346272_field_selector_column_chooser_options_clickable(self, driver):
        """C346272 Field Selector opens and column chooser options are clickable."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        # Click Field Selector / Column Chooser button
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        chooser_btn = container.find_element(
            By.CSS_SELECTOR,
            '[aria-label="Field Selector"], .dx-datagrid-column-chooser-button'
        )
        chooser_btn.click()

        # Wait for Column Chooser dialog
        chooser_dialog = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '[role="dialog"][aria-label="Column Chooser"]'
        )))

        # Click Select All twice (toggle all off then on)
        select_all = chooser_dialog.find_element(By.CSS_SELECTOR, '[aria-label="Select All"]')
        driver.execute_script("arguments[0].click();", select_all)
        wait_for_loading_screen(driver)
        driver.execute_script("arguments[0].click();", select_all)
        wait_for_loading_screen(driver)

        # Toggle each column checkbox twice
        column_labels = ["Activity", "Date", "Type", "User", "Contact", "Detail"]
        for label in column_labels:
            tree_item = chooser_dialog.find_element(
                By.CSS_SELECTOR, f'[role="treeitem"][aria-label="{label}"]'
            )
            assert tree_item.is_displayed()
            checkbox = tree_item.find_element(By.CSS_SELECTOR, ".dx-checkbox")
            driver.execute_script("arguments[0].click();", checkbox)
            driver.execute_script("arguments[0].click();", checkbox)
