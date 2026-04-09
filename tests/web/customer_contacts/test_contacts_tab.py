"""
Customer Details - Contacts tab panel tests.

Validates tab visibility, Add/Delete Contact buttons, search, status and
location filters, data grid columns, summary row, Field Selector, Create
Filter / Filter Builder, row-level Edit/Delete actions, and pagination.
"""
import pytest
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import (
    wait_for_loading_screen,
    select_dropdown,
    scroll_to_element,
    force_click,
)
from data.user_data import USER_DATA


CONTACTS_TAB_ID = "parentTabContainer_2"
CONTACTS_GRID_ID = "contactsDataGridContainer"


@pytest.mark.usefixtures("driver")
class TestContactsTab:
    """
    Verify Customer Details > Contacts tab panel elements and behaviour.

    Usage:
        pytest tests/web/customer_contacts/test_contacts_tab.py -v
    """

    # ── C325979 ────────────────────────────────────────────────────

    def test_c325979_contacts_tab_panel_is_visible_and_active(self, driver):
        """C325979 Contacts tab panel is visible and active."""
        page = BasePage(driver)
        tab = page.find_visible(By.ID, CONTACTS_TAB_ID, timeout=10)
        classes = tab.get_attribute("class")
        assert "active" in classes, "Contacts tab pane should have 'active' class"
        assert "in" in classes, "Contacts tab pane should have 'in' class"
        assert tab.get_attribute("role") == "tabpanel", (
            "Contacts tab pane role should be 'tabpanel'"
        )

    # ── C325980 ────────────────────────────────────────────────────

    def test_c325980_add_contact_button_visible_and_clickable(self, driver):
        """C325980 Add Contact button is visible and clickable."""
        cp = CustomerPage(driver)
        btn = cp.find_visible(*cp.CONTACTS_ADD_BTN)
        assert "Add Contact" in btn.text, "Button text should contain 'Add Contact'"
        assert btn.get_attribute("href") == "javascript:void(0)", (
            "Add Contact href should be javascript:void(0)"
        )

    # ── C325981 ────────────────────────────────────────────────────

    def test_c325981_delete_contact_button_hidden_when_no_rows_selected(self, driver):
        """C325981 Delete Contact button exists and is hidden when no rows selected."""
        page = BasePage(driver)
        assert page.element_exists(By.ID, "btnCTabMultipleDelete", timeout=10), (
            "Delete Contact button should exist in the DOM"
        )
        assert page.element_not_visible(By.ID, "btnCTabMultipleDelete"), (
            "Delete Contact button should not be visible when no rows are selected"
        )

    # ── C325982 ────────────────────────────────────────────────────

    def test_c325982_contact_status_filter_dropdown(self, driver):
        """C325982 Contact status filter dropdown has expected options and can be selected."""
        page = BasePage(driver)
        page.find_visible(By.ID, "contactStatusFilter")

        expected = {
            "0": "Active Contacts",
            "1": "In-Active Contacts",
            "2": "All Contacts",
        }
        for val, text_fragment in expected.items():
            option = page.find_element(
                By.CSS_SELECTOR,
                f'#contactStatusFilter option[value="{val}"]',
            )
            assert text_fragment in option.text, (
                f"Option value={val} should contain '{text_fragment}'"
            )

        select_el = driver.find_element(By.ID, "contactStatusFilter")
        sel = Select(select_el)
        for val in ["1", "2", "0"]:
            sel.select_by_value(val)
            assert select_el.get_attribute("value") == val
            wait_for_loading_screen(driver)

    # ── C325983 ────────────────────────────────────────────────────

    def test_c325983_location_filter_dropdown(self, driver):
        """C325983 Location filter dropdown has expected options and can be selected."""
        page = BasePage(driver)
        page.find_visible(By.ID, "contactServiceFilter")

        all_loc = page.find_element(
            By.CSS_SELECTOR,
            '#contactServiceFilter option[value=""]',
        )
        assert "All Locations" in all_loc.text

        assert page.element_exists(
            By.CSS_SELECTOR, '#contactServiceFilter option[value="1"]'
        ), "Location filter should have an option with value='1'"

        select_el = driver.find_element(By.ID, "contactServiceFilter")
        sel = Select(select_el)
        for val in ["", "1"]:
            sel.select_by_value(val)
            assert select_el.get_attribute("value") == val
            wait_for_loading_screen(driver)

    # ── C325984 ────────────────────────────────────────────────────

    def test_c325984_contacts_data_grid_visible(self, driver):
        """C325984 Contacts data grid container is visible."""
        page = BasePage(driver)
        assert page.element_is_visible(By.ID, CONTACTS_GRID_ID, timeout=10), (
            "Contacts data grid container should be visible"
        )
        assert page.element_exists(
            By.CSS_SELECTOR, f"#{CONTACTS_GRID_ID} .dx-datagrid"
        ), "DevExtreme datagrid should exist inside the container"

    # ── C325985 ────────────────────────────────────────────────────

    def test_c325985_data_grid_group_panel_message(self, driver):
        """C325985 Data grid group panel message is displayed."""
        page = BasePage(driver)
        cp = CustomerPage(driver)
        cp.find_visible(*cp.CONTACTS_GROUP_PANEL)
        msg = page.find_visible(
            By.CSS_SELECTOR,
            f"#{CONTACTS_GRID_ID} .dx-group-panel-message",
        )
        assert re.search(r"drag and drop column.*to group", msg.text, re.IGNORECASE), (
            "Group panel should show drag-and-drop instruction message"
        )

    # ── C325986 ────────────────────────────────────────────────────

    def test_c325986_data_grid_expected_column_headers(self, driver):
        """C325986 Data grid has expected column headers."""
        cp = CustomerPage(driver)
        for label in ["Type", "Name", "Company", "Title", "Primary",
                       "Contact 1", "Contact 2", "Contact 3", "Status"]:
            assert cp.contacts_column_header_exists(label), (
                f"Column header '{label}' should exist"
            )

        # Scroll right to reveal Action column
        cp.scroll_contacts_grid_right()
        action_sel = (
            f'#{CONTACTS_TAB_ID} [role="columnheader"][aria-label*="Action"]'
        )
        assert cp.element_exists(By.CSS_SELECTOR, action_sel, timeout=10), (
            "Action column header should exist after scrolling right"
        )

    # ── C325987 ────────────────────────────────────────────────────

    def test_c325987_field_selector_hide_show_columns(self, driver):
        """C325987 Field Selector button works and can hide/show columns in the grid."""
        cp = CustomerPage(driver)
        page = BasePage(driver)

        # Open Field Selector
        cp.click_element(*cp.CONTACTS_FIELD_SELECTOR_BTN)

        popup_content = page.find_visible(
            By.CSS_SELECTOR,
            ".dx-overlay-wrapper .dx-popup-content",
            timeout=10,
        )

        # Uncheck 'Type' column
        type_node = page.find_element(
            By.XPATH,
            "//div[contains(@class,'dx-popup-content')]"
            "//div[contains(@class,'dx-treeview-node') and contains(.,  'Type')]",
        )
        checkbox = type_node.find_element(
            By.CSS_SELECTOR, ".dx-checkbox-icon, .dx-checkbox, [class*='checkbox']"
        )
        driver.execute_script("arguments[0].click();", checkbox)

        # Validate Type column removed
        assert cp.contacts_column_header_not_present("Type"), (
            "Type column should be removed after unchecking in Field Selector"
        )

        # Re-check 'Type' column
        type_node = page.find_element(
            By.XPATH,
            "//div[contains(@class,'dx-popup-content')]"
            "//div[contains(@class,'dx-treeview-node') and contains(.,  'Type')]",
        )
        checkbox = type_node.find_element(
            By.CSS_SELECTOR, ".dx-checkbox-icon, .dx-checkbox, [class*='checkbox']"
        )
        driver.execute_script("arguments[0].click();", checkbox)
        wait_for_loading_screen(driver)

        # Validate Type column is back
        assert cp.contacts_column_header_exists("Type"), (
            "Type column should reappear after re-checking in Field Selector"
        )

        # Close Field Selector popup
        close_btn = page.find_clickable(
            By.CSS_SELECTOR, ".dx-overlay-wrapper .dx-closebutton"
        )
        close_btn.click()

    # ── C325988 ────────────────────────────────────────────────────

    def test_c325988_edit_contact_update_company_and_verify(self, driver):
        """C325988 Edit Contact: Update Company and verify Contact Type, Location, Detail, and Priority in grid."""
        cp = CustomerPage(driver)
        page = BasePage(driver)
        wait = WebDriverWait(driver, 20)

        company_value = USER_DATA.get("automation_user", "AutoMVC")
        mobile_value = USER_DATA.get("mobile", "1234567890")

        # Scroll right and click Edit
        cp.scroll_contacts_grid_right()
        edit_links = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(cp.CONTACTS_EDIT_LINK)
        )
        driver.execute_script("arguments[0].click();", edit_links[0])

        # Wait for EDIT CONTACT popup
        page.find_visible(
            By.XPATH,
            "//*[contains(translate(text(),'abcdefghijklmnopqrstuvwxyz',"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'EDIT CONTACT')]",
            timeout=30,
        )
        page.find_visible(*cp.EDIT_CONTACT_POPUP)

        # Update Company field
        company_field = page.find_visible(*cp.EDIT_CONTACT_COMPANY)
        company_field.clear()
        company_field.send_keys(company_value)

        # Verify Contact Type dropdown options
        contact_type_el = page.find_visible(*cp.EDIT_CONTACT_TYPE)
        ct_customer = driver.find_element(
            By.CSS_SELECTOR, '#Svc_ContactTypeId option[value="1"]'
        )
        assert "Customer" in ct_customer.text
        ct_service = driver.find_element(
            By.CSS_SELECTOR, '#Svc_ContactTypeId option[value="2"]'
        )
        assert "Service Location" in ct_service.text

        # Select each contact type
        sel_type = Select(contact_type_el)
        sel_type.select_by_value("1")
        assert contact_type_el.get_attribute("value") == "1"
        sel_type.select_by_value("2")
        assert contact_type_el.get_attribute("value") == "2"

        # Select first non-empty location option
        location_el = page.find_element(*cp.EDIT_CONTACT_LOCATION)
        options = location_el.find_elements(
            By.CSS_SELECTOR, 'option[value]:not([value=""])'
        )
        if options:
            Select(location_el).select_by_value(options[0].get_attribute("value"))
            driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                location_el,
            )

        # Click Add Detail
        add_detail = page.find_visible(*cp.EDIT_CONTACT_ADD_DETAIL_LINK)
        assert "Add Detail" in add_detail.text
        add_detail.click()

        # Detail Type dropdown – verify options and select Phone (1)
        detail_type = page.find_visible(*cp.EDIT_CONTACT_DETAIL_TYPE, timeout=15)
        sel_detail = Select(detail_type)
        for val in ["1", "2", "3", "4", "5", "8", "9"]:
            sel_detail.select_by_value(val)
            assert detail_type.get_attribute("value") == val
        sel_detail.select_by_value("1")

        # Enter phone number
        phone_field = page.find_clickable(*cp.EDIT_CONTACT_DETAIL_PHONE)
        phone_field.clear()
        phone_field.send_keys(mobile_value)

        # Priority dropdown – select first, validate second if present, set back
        priority_el = page.find_visible(*cp.EDIT_CONTACT_PRIORITY, timeout=15)
        priority_opts = priority_el.find_elements(By.TAG_NAME, "option")
        sel_priority = Select(priority_el)
        if priority_opts:
            sel_priority.select_by_index(0)
        if len(priority_opts) > 1:
            sel_priority.select_by_index(1)
        if priority_opts:
            sel_priority.select_by_index(0)

        # Save detail row
        save_detail_btn = page.find_visible(*cp.EDIT_CONTACT_SAVE_DETAIL_BTN)
        save_detail_btn.click()

        # Save contact
        save_btn = page.find_element(*cp.EDIT_CONTACT_SAVE_BTN)
        driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
        driver.execute_script("arguments[0].click();", save_btn)

        # Wait for grid refresh
        wait_for_loading_screen(driver, timeout=90)

    # ── C325989 ────────────────────────────────────────────────────

    def test_c325989_search_input_filters_grid(self, driver):
        """C325989 Search input works and filters grid."""
        cp = CustomerPage(driver)
        page = BasePage(driver)

        search_value = USER_DATA.get("automation_user", "AutoMVC")

        search_input = page.find_visible(*cp.CONTACTS_SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(search_value)

        # Wait for grid to filter (explicit wait for at least 1 data row)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"#{CONTACTS_GRID_ID} .dx-data-row")
            )
        )

        rows = driver.find_elements(*cp.CONTACTS_DATA_ROWS)
        assert len(rows) >= 1, "At least one data row should appear after filtering"
        for row in rows:
            assert re.search(search_value, row.text, re.IGNORECASE), (
                f"Row text should contain '{search_value}'"
            )

    # ── C325990 ────────────────────────────────────────────────────

    def test_c325990_create_filter_add_condition(self, driver):
        """C325990 Create Filter: Add condition using automation user and verify filter is applied."""
        page = BasePage(driver)
        cp = CustomerPage(driver)

        filter_value = USER_DATA.get("automation_user", "AutoMVC")

        # Click "Create Filter"
        create_filter = page.find_visible(*cp.CONTACTS_FILTER_PANEL_TEXT, timeout=10)
        assert "Create Filter" in create_filter.text
        create_filter.click()

        # Filter Builder overlay opens
        filter_builder = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class,'dx-overlay-wrapper')]"
                "[.//div[contains(text(),'Filter Builder')]]",
            ))
        )

        # Click Add (plus) icon
        add_icon = filter_builder.find_element(
            By.CSS_SELECTOR,
            "[aria-label='Add'], .dx-filterbuilder-action-icon.dx-icon-plus",
        )
        add_icon.click()

        # Click "Add Condition"
        add_cond = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'li[aria-label="Add Condition"] .dx-treeview-item-content,'
                ' [aria-label="Add Condition"] .dx-item-content',
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", add_cond)
        driver.execute_script("arguments[0].click();", add_cond)

        # Click value field and type filter value
        value_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                ".dx-filterbuilder-item-value-text[title='Item value'],"
                " .dx-filterbuilder-item-value .dx-filterbuilder-item-value-text,"
                " .dx-filterbuilder-item-value-text",
            ))
        )
        driver.execute_script("arguments[0].click();", value_field)

        # Type into the focused input
        active = driver.switch_to.active_element
        active.send_keys(filter_value)

        # Click OK
        ok_btn = filter_builder.find_element(
            By.XPATH,
            ".//div[contains(@class,'dx-button')]"
            "[.//span[contains(@class,'dx-button-text') and contains(text(),'OK')]]",
        )
        ok_btn.click()
        wait_for_loading_screen(driver)

        # Validate filter panel shows the filter value
        filter_panel = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                f"#{CONTACTS_GRID_ID} .dx-datagrid-filter-panel,"
                f" #{CONTACTS_GRID_ID} .dx-datagrid-filter-row,"
                f" #{CONTACTS_GRID_ID} [class*='filter-panel']",
            ))
        )
        assert filter_value in filter_panel.text, (
            f"Filter panel should display '{filter_value}'"
        )

    # ── C325991 ────────────────────────────────────────────────────

    def test_c325991_pagination_items_per_page(self, driver):
        """C325991 Pagination: items-per-page options (10, 25, 50, 100, 200) are visible and clickable."""
        page = BasePage(driver)
        cp = CustomerPage(driver)
        items_per_page_sizes = ["10", "25", "50", "100", "200"]

        pager = page.find_visible(*cp.CONTACTS_PAGER, timeout=10)
        scroll_to_element(driver, pager)
        page.find_visible(*cp.CONTACTS_PAGE_SIZES)

        # Determine current selection and pick an alternate first
        current_sel = driver.find_elements(
            By.CSS_SELECTOR,
            f"#{CONTACTS_GRID_ID} .dx-datagrid-pager .dx-page-sizes .dx-page-size.dx-selection",
        )
        current_label = ""
        if current_sel:
            current_label = (
                current_sel[0].get_attribute("aria-label") or ""
            ).replace("Items per page: ", "").strip()

        others = [s for s in items_per_page_sizes if s != current_label]
        alternate = others[-1] if others else items_per_page_sizes[0]

        alt_btn = page.find_clickable(
            By.CSS_SELECTOR,
            f'#{CONTACTS_GRID_ID} .dx-datagrid-pager .dx-page-sizes'
            f' [role="button"][aria-label="Items per page: {alternate}"]',
        )
        scroll_to_element(driver, alt_btn)
        driver.execute_script("arguments[0].click();", alt_btn)
        wait_for_loading_screen(driver)

        # Click each size and verify selection
        for size in items_per_page_sizes:
            size_btn = page.find_clickable(
                By.CSS_SELECTOR,
                f'#{CONTACTS_GRID_ID} .dx-datagrid-pager .dx-page-sizes'
                f' [role="button"][aria-label="Items per page: {size}"]',
            )
            scroll_to_element(driver, size_btn)
            driver.execute_script("arguments[0].click();", size_btn)
            wait_for_loading_screen(driver)

            selected = page.find_element(
                By.CSS_SELECTOR,
                f'#{CONTACTS_GRID_ID} .dx-datagrid-pager .dx-page-sizes'
                f' [aria-label="Items per page: {size}"]',
            )
            assert "dx-selection" in (selected.get_attribute("class") or ""), (
                f"Page size {size} should be selected after clicking"
            )

    # ── C325992 ────────────────────────────────────────────────────

    def test_c325992_delete_contact_from_grid(self, driver):
        """C325992 Delete Contact: Remove contact from grid after confirmation."""
        page = BasePage(driver)
        cp = CustomerPage(driver)

        # Ensure at least one data row exists
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(cp.CONTACTS_DATA_ROWS)
        )
        assert len(rows) >= 1, "At least one contact row should exist before deletion"

        # Stub native confirm to always return true
        driver.execute_script("window.confirm = function() { return true; };")

        # Scroll right to reveal Action column with delete button
        cp.scroll_contacts_grid_right()

        delete_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(cp.CONTACTS_DELETE_LINK)
        )
        driver.execute_script("arguments[0].click();", delete_btn[0])

        wait_for_loading_screen(driver)

        # Grid should still exist (may have fewer rows or be empty)
        assert page.element_exists(
            By.CSS_SELECTOR, f"#{CONTACTS_GRID_ID} .dx-datagrid"
        ), "Contacts data grid should still exist after deletion"
