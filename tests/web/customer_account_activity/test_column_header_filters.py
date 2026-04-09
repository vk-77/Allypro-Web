"""
Customer Details - Account Activity column header filter tests.

Validates search, clear, checkbox toggle, Cancel, and OK actions on each
column header filter (Activity, Date, Type, User, Contact, Detail).
"""
import re
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen
from data.user_data import USER_DATA


ACCOUNT_ACTIVITY_CONTAINER = "#parentTabContainer_4"
ACCOUNT_ACTIVITY_DATA_ROW = (
    "#parentTabContainer_4 .dx-datagrid-rowsview "
    "table.dx-datagrid-table-fixed tbody tr.dx-data-row"
)
FILTER_OPTIONS_DIALOG = '[role="dialog"][aria-label="Filter options"]'
SEARCH_INPUT = 'input.dx-texteditor-input[aria-label="Search"]'


def _open_column_header_filter(driver, column_name, timeout=10):
    """Click the filter-options icon for the given column header."""
    wait = WebDriverWait(driver, timeout)
    btn = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        f'{ACCOUNT_ACTIVITY_CONTAINER} span[aria-label="Show filter options for column \'{column_name}\'"]'
    )))
    btn.click()
    # Wait for filter options dialog
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)))


def _type_in_filter_search(driver, text):
    """Type text into the filter options search input."""
    dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
    search = dialog.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
    search.click()
    search.send_keys(text)


def _clear_filter_search(driver):
    """Click the clear icon in the filter options search field."""
    dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
    clear_btn = dialog.find_element(By.CSS_SELECTOR, ".dx-clear-button-area")
    clear_btn.click()


def _get_filter_search_value(driver):
    """Return the current value of the filter options search input."""
    dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
    search = dialog.find_element(By.CSS_SELECTOR, SEARCH_INPUT)
    return search.get_attribute("value")


def _click_list_item_checkbox(driver, text):
    """Find a list item containing text and click its checkbox. Returns the checkbox element."""
    dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
    item = dialog.find_element(
        By.XPATH,
        f".//*[contains(@class,'dx-list-item-content') and contains(text(),'{text}')]"
        f"/ancestor::*[contains(@class,'dx-list-item')][1]"
    )
    checkbox = item.find_element(By.CSS_SELECTOR, '[role="checkbox"]')
    assert checkbox.is_displayed()
    return checkbox


def _click_treeview_checkbox(driver, text):
    """Find a tree-view item containing text and click its checkbox. Returns the checkbox element."""
    dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
    tree_item = dialog.find_element(
        By.XPATH,
        f".//*[contains(@class,'dx-treeview-item') and contains(text(),'{text}')]"
    )
    checkbox = tree_item.find_element(By.CSS_SELECTOR, '[role="checkbox"]')
    assert checkbox.is_displayed()
    return checkbox


def _click_dialog_button(driver, label):
    """Click a button inside the filter options dialog by aria-label (OK, Cancel)."""
    dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
    btn = dialog.find_element(By.CSS_SELECTOR, f'[role="button"][aria-label="{label}"]')
    btn.click()


def _get_first_row_detail_term(driver):
    """Extract a search term (>=3 chars) from the first data row Detail column."""
    wait = WebDriverWait(driver, 10)
    first_row = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)))
    detail_cell = first_row.find_element(By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="6"]')
    cleaned = re.sub(r"\s+", " ", detail_cell.text).strip()
    words = cleaned.split()
    term = next((w for w in words if len(w) >= 3), cleaned[:min(8, len(cleaned))])
    assert len(term) > 2, "Detail filter search term must be longer than 2 characters"
    return term


# ======================================================================
# Test class
# ======================================================================

@pytest.mark.usefixtures("driver")
class TestAccountActivityColumnHeaderFilters:
    """Account Activity column header filter tests.

    Usage:
        pytest tests/web/customer_account_activity/test_column_header_filters.py -v
    """

    # -- Activity column ────────────────────────────────────────────

    def test_c346273_activity_header_filter_search_refines(self, driver):
        """C346273 Activity column header filter - open Filter options, type Customer in list search refines items."""
        _open_column_header_filter(driver, "Activity")
        _type_in_filter_search(driver, "Customer")
        dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
        items = dialog.find_elements(By.CSS_SELECTOR, ".dx-list-item .dx-list-item-content")
        assert any("Customer" in item.text for item in items)

    def test_c346274_activity_header_filter_clear_empties_search(self, driver):
        """C346274 Activity column header filter - clear icon empties the Filter options search field."""
        _open_column_header_filter(driver, "Activity")
        _type_in_filter_search(driver, "Customer")
        assert _get_filter_search_value(driver) == "Customer"
        _clear_filter_search(driver)
        assert _get_filter_search_value(driver) == ""

    def test_c346275_activity_header_filter_checkbox_toggles(self, driver):
        """C346275 Activity column header filter - Customer row checkbox is visible and toggles checked state."""
        _open_column_header_filter(driver, "Activity")
        checkbox = _click_list_item_checkbox(driver, "Customer")
        assert checkbox.get_attribute("aria-checked") == "false"
        checkbox.click()
        assert checkbox.get_attribute("aria-checked") == "true"

    def test_c346301_activity_header_filter_cancel_closes(self, driver):
        """C346301 Activity column header filter - Cancel closes Filter options dialog."""
        _open_column_header_filter(driver, "Activity")
        _click_dialog_button(driver, "Cancel")

    def test_c346302_activity_header_filter_ok_applies(self, driver):
        """C346302 Activity column header filter - OK applies selection and closes Filter options dialog."""
        _open_column_header_filter(driver, "Activity")
        checkbox = _click_list_item_checkbox(driver, "Customer")
        checkbox.click()
        _click_dialog_button(driver, "OK")

    # -- Date column ────────────────────────────────────────────────

    def test_c346276_date_header_filter_search_refines(self, driver):
        """C346276 Date column header filter - open Filter options, type 2026 in list search refines items."""
        _open_column_header_filter(driver, "Date")
        _type_in_filter_search(driver, "2026")
        dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
        tree_item = dialog.find_element(
            By.XPATH,
            ".//*[contains(@class,'dx-treeview-item') and contains(text(),'2026')]"
        )
        assert tree_item.is_displayed()

    def test_c346277_date_header_filter_clear_empties_search(self, driver):
        """C346277 Date column header filter - clear icon empties the Filter options search field."""
        _open_column_header_filter(driver, "Date")
        _type_in_filter_search(driver, "2026")
        assert _get_filter_search_value(driver) == "2026"
        _clear_filter_search(driver)
        assert _get_filter_search_value(driver) == ""

    def test_c346278_date_header_filter_checkbox_toggles(self, driver):
        """C346278 Date column header filter - list row checkbox is visible and toggles checked state."""
        _open_column_header_filter(driver, "Date")
        _type_in_filter_search(driver, "2026")
        checkbox = _click_treeview_checkbox(driver, "2026")
        assert checkbox.get_attribute("aria-checked") == "false"
        checkbox.click()
        assert checkbox.get_attribute("aria-checked") == "true"

    def test_c346279_date_header_filter_cancel_closes(self, driver):
        """C346279 Date column header filter - Cancel closes Filter options dialog."""
        _open_column_header_filter(driver, "Date")
        _click_dialog_button(driver, "Cancel")

    def test_c346280_date_header_filter_ok_applies(self, driver):
        """C346280 Date column header filter: OK applies selection and closes Filter options dialog."""
        _open_column_header_filter(driver, "Date")
        _type_in_filter_search(driver, "2026")
        checkbox = _click_treeview_checkbox(driver, "2026")
        checkbox.click()
        _click_dialog_button(driver, "OK")

    # -- Type column ────────────────────────────────────────────────

    def test_c346281_type_header_filter_search_refines(self, driver):
        """C346281 Type column header filter: open Filter options, type Automation in list search refines items."""
        _open_column_header_filter(driver, "Type")
        _type_in_filter_search(driver, "Automation")
        dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
        items = dialog.find_elements(By.CSS_SELECTOR, ".dx-list-item .dx-list-item-content")
        assert any("Automation" in item.text for item in items)

    def test_c346282_type_header_filter_clear_empties_search(self, driver):
        """C346282 Type column header filter: clear icon empties the Filter options search field."""
        _open_column_header_filter(driver, "Type")
        _type_in_filter_search(driver, "Automation")
        assert _get_filter_search_value(driver) == "Automation"
        _clear_filter_search(driver)
        assert _get_filter_search_value(driver) == ""

    def test_c346283_type_header_filter_checkbox_toggles(self, driver):
        """C346283 Type column header filter - Automation row checkbox is visible and toggles checked state."""
        _open_column_header_filter(driver, "Type")
        checkbox = _click_list_item_checkbox(driver, "Automation")
        assert checkbox.get_attribute("aria-checked") == "false"
        checkbox.click()
        assert checkbox.get_attribute("aria-checked") == "true"

    def test_c346284_type_header_filter_cancel_closes(self, driver):
        """C346284 Type column header filter - Cancel closes Filter options dialog."""
        _open_column_header_filter(driver, "Type")
        _click_dialog_button(driver, "Cancel")

    def test_c346285_type_header_filter_ok_applies(self, driver):
        """C346285 Type column header filter - OK applies selection and closes Filter options dialog."""
        _open_column_header_filter(driver, "Type")
        checkbox = _click_list_item_checkbox(driver, "Automation")
        checkbox.click()
        _click_dialog_button(driver, "OK")

    # -- User column ────────────────────────────────────────────────

    def test_c346286_user_header_filter_search_refines(self, driver):
        """C346286 User column header filter - open Filter options, type automation user in list search refines items."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "User")
        _type_in_filter_search(driver, term)
        dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
        items = dialog.find_elements(By.CSS_SELECTOR, ".dx-list-item .dx-list-item-content")
        assert any(term in item.text for item in items)

    def test_c346287_user_header_filter_clear_empties_search(self, driver):
        """C346287 User column header filter - clear icon empties the Filter options search field."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "User")
        _type_in_filter_search(driver, term)
        assert _get_filter_search_value(driver) == term
        _clear_filter_search(driver)
        assert _get_filter_search_value(driver) == ""

    def test_c346288_user_header_filter_checkbox_toggles(self, driver):
        """C346288 User column header filter - automation user row checkbox is visible and toggles checked state."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "User")
        checkbox = _click_list_item_checkbox(driver, term)
        assert checkbox.get_attribute("aria-checked") == "false"
        checkbox.click()
        assert checkbox.get_attribute("aria-checked") == "true"

    def test_c346289_user_header_filter_cancel_closes(self, driver):
        """C346289 User column header filter - Cancel closes Filter options dialog."""
        _open_column_header_filter(driver, "User")
        _click_dialog_button(driver, "Cancel")

    def test_c346290_user_header_filter_ok_applies(self, driver):
        """C346290 User column header filter - OK applies selection and closes Filter options dialog."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "User")
        checkbox = _click_list_item_checkbox(driver, term)
        checkbox.click()
        _click_dialog_button(driver, "OK")

    # -- Contact column ─────────────────────────────────────────────

    def test_c346291_contact_header_filter_search_refines(self, driver):
        """C346291 Contact column header filter - open Filter options, type automation user in list search refines items."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "Contact")
        _type_in_filter_search(driver, term)
        dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
        items = dialog.find_elements(By.CSS_SELECTOR, ".dx-list-item .dx-list-item-content")
        assert any(term in item.text for item in items)

    def test_c346292_contact_header_filter_clear_empties_search(self, driver):
        """C346292 Contact column header filter - clear icon empties the Filter options search field."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "Contact")
        _type_in_filter_search(driver, term)
        assert _get_filter_search_value(driver) == term
        _clear_filter_search(driver)
        assert _get_filter_search_value(driver) == ""

    def test_c346293_contact_header_filter_checkbox_toggles(self, driver):
        """C346293 Contact column header filter - automation user row checkbox is visible and toggles checked state."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "Contact")
        checkbox = _click_list_item_checkbox(driver, term)
        assert checkbox.get_attribute("aria-checked") == "false"
        checkbox.click()
        assert checkbox.get_attribute("aria-checked") == "true"

    def test_c346294_contact_header_filter_cancel_closes(self, driver):
        """C346294 Contact column header filter - Cancel closes Filter options dialog."""
        _open_column_header_filter(driver, "Contact")
        _click_dialog_button(driver, "Cancel")

    def test_c346295_contact_header_filter_ok_applies(self, driver):
        """C346295 Contact column header filter - OK applies selection and closes Filter options dialog."""
        term = USER_DATA["automation_user"]
        _open_column_header_filter(driver, "Contact")
        checkbox = _click_list_item_checkbox(driver, term)
        checkbox.click()
        _click_dialog_button(driver, "OK")

    # -- Detail column ──────────────────────────────────────────────

    def test_c346296_detail_header_filter_search_refines(self, driver):
        """C346296 Detail column header filter - open Filter options, type term from first row in list search refines items."""
        term = _get_first_row_detail_term(driver)
        _open_column_header_filter(driver, "Detail")
        _type_in_filter_search(driver, term)
        dialog = driver.find_element(By.CSS_SELECTOR, FILTER_OPTIONS_DIALOG)
        items = dialog.find_elements(By.CSS_SELECTOR, ".dx-list-item .dx-list-item-content")
        assert any(term in item.text for item in items)

    def test_c346297_detail_header_filter_clear_empties_search(self, driver):
        """C346297 Detail column header filter - clear icon empties the Filter options search field."""
        term = _get_first_row_detail_term(driver)
        _open_column_header_filter(driver, "Detail")
        _type_in_filter_search(driver, term)
        assert _get_filter_search_value(driver) == term
        _clear_filter_search(driver)
        assert _get_filter_search_value(driver) == ""

    def test_c346298_detail_header_filter_checkbox_toggles(self, driver):
        """C346298 Detail column header filter - list row checkbox is visible and toggles checked state."""
        term = _get_first_row_detail_term(driver)
        _open_column_header_filter(driver, "Detail")
        checkbox = _click_list_item_checkbox(driver, term)
        assert checkbox.get_attribute("aria-checked") == "false"
        checkbox.click()
        assert checkbox.get_attribute("aria-checked") == "true"

    def test_c346299_detail_header_filter_cancel_closes(self, driver):
        """C346299 Detail column header filter - Cancel closes Filter options dialog."""
        _open_column_header_filter(driver, "Detail")
        _click_dialog_button(driver, "Cancel")

    def test_c346300_detail_header_filter_ok_applies(self, driver):
        """C346300 Detail column header filter - OK applies selection and closes Filter options dialog."""
        term = _get_first_row_detail_term(driver)
        _open_column_header_filter(driver, "Detail")
        checkbox = _click_list_item_checkbox(driver, term)
        checkbox.click()
        _click_dialog_button(driver, "OK")
