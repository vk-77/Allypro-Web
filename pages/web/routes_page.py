"""
Page object for the Elements Routes pages (Route Optimization, Route Log, Batch History).
"""
from selenium.webdriver.common.by import By

from .base_web_page import BaseWebPage


class RoutesPage(BaseWebPage):
    """
    Page object for Routes section pages.
    """

    # ── Locators ──────────────────────────────────────────────────

    PAGE_TITLE = (By.CSS_SELECTOR, ".pageTitle")

    # Route Optimization
    ROUTE_OPTIMIZATION_MENU = (By.ID, "Active_24")
    ROUTE_NAME_FILTER = (By.CSS_SELECTOR, "#RouteOptimization input[placeholder*='Route']")
    OPTIMIZE_BTN = (By.CSS_SELECTOR, '[onclick*="OptimizeRoute"], #btnOptimize')
    BATCH_HISTORY_BTN = (By.CSS_SELECTOR, '[onclick*="BatchHistory"], #btnBatchHistory')

    # Route Log
    ROUTE_LOG_MENU = (By.ID, "Active_51")
    ROUTE_LOG_TABLE = (By.ID, "RouteLogListTable")

    # Data Grid
    DATA_GRID = (By.CSS_SELECTOR, ".dx-datagrid")
    DATA_ROWS = (By.CSS_SELECTOR, ".dx-data-row")

    # ── Actions ───────────────────────────────────────────────────

    def open_route_optimization(self):
        """Click Route Optimization submenu."""
        self.click_element(*self.ROUTE_OPTIMIZATION_MENU)
        self.wait_for_loading_screen()

    def open_route_log(self):
        """Click Route Log submenu."""
        self.click_element(*self.ROUTE_LOG_MENU)
        self.wait_for_loading_screen()

    def get_page_title(self):
        """Return page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def is_data_grid_visible(self):
        """Return True if data grid is visible."""
        return self.element_is_visible(*self.DATA_GRID)

    def get_data_row_count(self):
        """Return count of data rows in the grid."""
        return len(self.find_elements(*self.DATA_ROWS))
