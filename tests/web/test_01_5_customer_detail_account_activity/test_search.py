"""
Customer Details - Account Activity search tests.

"""
import re
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen
from data.user_data import USER_DATA


ACCOUNT_ACTIVITY_CONTAINER = "#parentTabContainer_4"
ACCOUNT_ACTIVITY_DATA_ROW = (
    "#parentTabContainer_4 .dx-datagrid-rowsview "
    "table.dx-datagrid-table-fixed tbody tr.dx-data-row"
)
FILTER_ROW = "#parentTabContainer_4 tr.dx-datagrid-filter-row"
GRID_SEARCH_INPUT = (
    f'{ACCOUNT_ACTIVITY_CONTAINER} '
    'input.dx-texteditor-input[placeholder="Search..."][aria-label="Search in the data grid"]'
)


def _type_into_filter_cell(driver, col_index, term, role="textbox"):
    """Click and type into a filter-row cell by column index.

    Mirrors the Cypress pattern of typing the first char, waiting for
    loading, then typing the rest.
    """
    wait = WebDriverWait(driver, 15)
    cell_selector = (
        f'{FILTER_ROW} td[role="gridcell"][aria-label="Filter cell"]'
        f'[aria-colindex="{col_index}"] '
        f'input.dx-texteditor-input[aria-label="Filter cell"][role="{role}"]'
    )

    input_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cell_selector)))
    input_el.click()
    input_el.send_keys(term[0])
    wait_for_loading_screen(driver)

    input_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cell_selector)))
    input_el.send_keys(term[1:])
    assert input_el.get_attribute("value") == term
    wait_for_loading_screen(driver)


@pytest.mark.usefixtures("driver")
class TestAccountActivitySearch:
    """Account Activity search and filter-row tests.

    Usage:
        pytest tests/web/test_01_5_customer_detail_account_activity/test_search.py -v
    """

    # ------------------------------------------------------------------
    # C346310 - Search activity button
    # ------------------------------------------------------------------
    def test_c346310_search_activity_button(self, driver):
        """C346310 Account Activity search - Verify search activity button."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        search_input = wait.until(EC.visibility_of_element_located((By.ID, "txtsearchActivity")))
        assert search_input.get_attribute("placeholder") == "Search"

        search_input.clear()
        search_input.send_keys("Auto")

        search_btn = wait.until(EC.element_to_be_clickable((By.ID, "SearchWithActivityFilterBtn")))
        search_btn.click()
        wait_for_loading_screen(driver)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1, "Should have at least one data row"

        for row in rows:
            assert USER_DATA["automation_user"] in row.text

    # ------------------------------------------------------------------
    # C346311 - Field Selector / Column Chooser search
    # ------------------------------------------------------------------
    def test_c346311_field_selector_search_columns(self, driver):
        """C346311 Field Selector - open column chooser, search columns for Activity, Activity tree item stays visible."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)

        # Click column chooser icon
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        chooser_icon = container.find_element(By.CSS_SELECTOR, "i.dx-icon-column-chooser")
        chooser_icon.click()

        # Wait for Column Chooser dialog
        chooser_dialog = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '[role="dialog"][aria-label="Column Chooser"]'
        )))

        # Find and type into the search input
        search_input = chooser_dialog.find_element(
            By.CSS_SELECTOR,
            'input.dx-texteditor-input[placeholder="Search column"][aria-label="Search"]'
        )
        search_input.click()
        search_input.send_keys("A")
        wait_for_loading_screen(driver)

        search_input.send_keys("ctivity")
        assert search_input.get_attribute("value") == "Activity"

        # Verify Activity tree item is visible
        activity_item = chooser_dialog.find_element(
            By.CSS_SELECTOR, '[role="treeitem"][aria-label="Activity"]'
        )
        assert activity_item.is_displayed()

    # ------------------------------------------------------------------
    # C346312 - Data grid search
    # ------------------------------------------------------------------
    def test_c346312_data_grid_search_by_automation_user(self, driver):
        """C346312 Account Activity data grid search - type automation user in grid search, rows match."""
        page = BaseWebPage(driver)
        wait = WebDriverWait(driver, 15)
        term = USER_DATA["automation_user"]

        search_input = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, GRID_SEARCH_INPUT
        )))
        search_input.click()
        search_input.send_keys(term[0])
        wait_for_loading_screen(driver)

        search_input = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, GRID_SEARCH_INPUT
        )))
        search_input.send_keys(term[1:])
        assert search_input.get_attribute("value") == term
        wait_for_loading_screen(driver)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1, "Should have at least one matching row"

        for row in rows:
            assert term in row.text

    # ------------------------------------------------------------------
    # C346313 - Filter row: User column
    # ------------------------------------------------------------------
    def test_c346313_filter_row_user_column(self, driver):
        """C346313 Account Activity filter row - User column filters by automation user."""
        wait = WebDriverWait(driver, 15)
        term = USER_DATA["automation_user"]

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_ROW)))
        _type_into_filter_cell(driver, 4, term)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1

        for row in rows:
            user_cell = row.find_element(By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="4"]')
            assert term in user_cell.text

    # ------------------------------------------------------------------
    # C346314 - Filter row: Type column
    # ------------------------------------------------------------------
    def test_c346314_filter_row_type_column(self, driver):
        """C346314 Account Activity filter row - Type column filters by Automation."""
        wait = WebDriverWait(driver, 15)
        term = "Automation"

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_ROW)))
        _type_into_filter_cell(driver, 3, term)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1

    # ------------------------------------------------------------------
    # C346315 - Filter row: Activity column
    # ------------------------------------------------------------------
    def test_c346315_filter_row_activity_column(self, driver):
        """C346315 Account Activity filter row - Activity column filters by Customer."""
        wait = WebDriverWait(driver, 15)
        term = "Customer"

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_ROW)))
        _type_into_filter_cell(driver, 1, term)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1

        for row in rows:
            activity_cell = row.find_element(By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="1"]')
            assert term in activity_cell.text

    # ------------------------------------------------------------------
    # C346316 - Filter row: Contact column
    # ------------------------------------------------------------------
    def test_c346316_filter_row_contact_column(self, driver):
        """C346316 Account Activity filter row - Contact column filters by automation user."""
        wait = WebDriverWait(driver, 15)
        term = USER_DATA["automation_user"]

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_ROW)))
        _type_into_filter_cell(driver, 5, term)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1

        for row in rows:
            contact_cell = row.find_element(By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="5"]')
            assert term in contact_cell.text

    # ------------------------------------------------------------------
    # C346317 - Filter row: Detail column
    # ------------------------------------------------------------------
    def test_c346317_filter_row_detail_column(self, driver):
        """C346317 Account Activity filter row - Detail column filters using first row detail text."""
        wait = WebDriverWait(driver, 15)

        # Get the detail text from the first row before filtering
        first_row = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW
        )))
        detail_cell = first_row.find_element(
            By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="6"]'
        )
        assert detail_cell.is_displayed()
        cleaned = re.sub(r"\s+", " ", detail_cell.text).strip()
        assert len(cleaned) > 2, "First row Detail cell should have text"

        words = cleaned.split()
        term = next((w for w in words if len(w) >= 3), cleaned[:min(8, len(cleaned))])

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_ROW)))
        _type_into_filter_cell(driver, 6, term)

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1

    # ------------------------------------------------------------------
    # C346318 - Filter row: Date column
    # ------------------------------------------------------------------
    def test_c346318_filter_row_date_column(self, driver):
        """C346318 Account Activity filter row - Date column filters using first row date text."""
        wait = WebDriverWait(driver, 15)

        # Get date from first row
        first_row = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW
        )))
        date_cell = first_row.find_element(
            By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="2"]'
        )
        assert date_cell.is_displayed()
        cleaned = re.sub(r"\s+", " ", date_cell.text).strip()
        assert len(cleaned) > 0, "First row Date cell should have text"

        year_match = re.search(r"\d{4}", cleaned)
        term = year_match.group(0) if year_match else cleaned[:min(6, len(cleaned))]
        assert len(term) > 0

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, FILTER_ROW)))
        # Date column uses combobox role
        _type_into_filter_cell(driver, 2, term, role="combobox")

        rows = driver.find_elements(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_DATA_ROW)
        assert len(rows) >= 1

        for row in rows:
            date_cell = row.find_element(By.CSS_SELECTOR, 'td[role="gridcell"][aria-colindex="2"]')
            assert term in date_cell.text
