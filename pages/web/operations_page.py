"""
Page object for the Elements Operations pages (Routing Queue).
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_web_page import BaseWebPage


class OperationsPage(BaseWebPage):
    """
    Page object for Operations section pages.
    """

    # ── Locators ──────────────────────────────────────────────────

    PAGE_TITLE = (By.CSS_SELECTOR, ".pageTitle")
    ROUTING_QUEUE_MENU = (By.ID, "Active_23")
    ROUTING_ASSIGNMENT_MENU = (By.ID, "Active_24")

    ROUTING_QUEUE_TABLE = (By.CSS_SELECTOR, "#RoutingQueueTable, .dx-datagrid")
    DATA_ROWS = (By.CSS_SELECTOR, ".dx-data-row")

    # Routing Assignment
    SERVICE_CHECKBOX = (By.CSS_SELECTOR, '[name="chkSelectServiceUID"]')
    ROUTE_SELECTED_BTN = (By.ID, "divRouteSelected")
    DAY_OF_WEEK_SELECT = (By.ID, "ddlGridDayOfWeek_1")
    SELECT_ROUTE_BTN = (By.CSS_SELECTOR, '[title="Select Route"]')
    ROUTE_SEARCH_FIELD = (By.CSS_SELECTOR, '[class*="-search__field"]')
    VALIDATE_ROUTE_BTN = (By.CSS_SELECTOR, '[onclick="return validateRouteQueue();"]')

    SUCCESS_MESSAGE = (By.ID, "divSucessContent")

    # ── Actions ───────────────────────────────────────────────────

    def open_routing_queue(self):
        """Click Routing Queue submenu."""
        self.click_element(*self.ROUTING_QUEUE_MENU)
        self.wait_for_loading_screen()

    def open_routing_assignment(self):
        """Click Routing Assignment submenu (Active_24)."""
        self.click_element(*self.ROUTING_ASSIGNMENT_MENU)
        self.wait_for_loading_screen()

    def get_page_title(self):
        """Return page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def is_table_visible(self):
        """Return True if routing queue table is visible."""
        return self.element_is_visible(*self.ROUTING_QUEUE_TABLE)
