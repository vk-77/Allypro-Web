"""
Search page object for Global Search and Advanced Filters.

Handles keyword search, result-grid verification, and advanced
filter fields (customer ID, name, location, service, address).
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base_web_page import BasePage


class SearchPage(BasePage):
    """Page object for Global Search and Advanced Filter Search."""

    # ── Locators ──────────────────────────────────────────────────

    SEARCH_INPUT = (By.ID, "txtSearchResultItemFromMenu")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".global-search-btn, #btnGlobalSearch")
    ADVANCED_FILTER_BTN = (By.CSS_SELECTOR, '[onclick*="ShowAdvancedSearch"], #btnAdvancedSearch')

    # Search result grid
    RESULT_GRID = (By.CSS_SELECTOR, "#searchResultGrid, .dx-datagrid")
    RESULT_ROWS = (By.CSS_SELECTOR, ".dx-data-row")
    NO_DATA_TEXT = "No data"

    # Advanced search filters
    FILTER_CUSTOMER_ID = (By.ID, "txtCustomerID")
    FILTER_NAME = (By.ID, "txtCustomerName")
    FILTER_LOCATION_ID = (By.ID, "txtLocationID")
    FILTER_SERVICE_ID = (By.ID, "txtServiceID")
    FILTER_ADDRESS = (By.ID, "txtAddress")

    # ── Actions ───────────────────────────────────────────────────

    def search(self, query):
        """Enter search query and submit."""
        field = self.find_clickable(*self.SEARCH_INPUT)
        field.clear()
        field.send_keys(query)
        field.send_keys(Keys.ENTER)
        self.wait_for_loading_screen()

    def click_search_button(self):
        """Click the search button."""
        self.click_element(*self.SEARCH_BUTTON)
        self.wait_for_loading_screen()

    def is_result_grid_visible(self):
        """Return True if search result grid is visible."""
        return self.element_is_visible(*self.RESULT_GRID)

    def get_result_row_count(self):
        """Return the number of result rows."""
        return len(self.find_elements(*self.RESULT_ROWS))

    def has_results(self):
        """Return True if search produced results."""
        return self.get_result_row_count() > 0
