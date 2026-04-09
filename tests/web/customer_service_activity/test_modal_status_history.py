"""
Customer Details - Service Activity work order Status History tab tests.

Validates the Status History table visibility and column headers (Date,
User, Status Description) on the Status History tab.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT


STATUS_HISTORY_HEADER_TITLES = ["Date", "User", "Status Description"]


def _open_status_history_tab(driver):
    """Open today's work order and activate the Status History tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_STATUS_HISTORY, page.WO_PANE_STATUS_HISTORY)
    return page


@pytest.mark.usefixtures("driver")
class TestModalStatusHistory:
    """
    Service Activity tab - work order Status History tab.

    """

    def test_c339682_status_history_tab_table_visible(self, driver):
        """C339682 Status History tab: table is visible."""
        page = _open_status_history_tab(driver)
        pane = page.find_visible(*page.WO_PANE_STATUS_HISTORY, timeout=15)
        assert "active" in pane.get_attribute("class")
        tables = driver.find_elements(*page.WO_STATUS_HISTORY_TABLE)
        visible_tables = [t for t in tables if t.is_displayed()]
        assert len(visible_tables) >= 1

    def test_c339643_status_history_tab_table_headers(self, driver):
        """C339643 Status History tab: Verify table headers Date, User, and Status Description are present."""
        page = _open_status_history_tab(driver)
        tables = driver.find_elements(*page.WO_STATUS_HISTORY_TABLE)
        visible_table = next((t for t in tables if t.is_displayed()), None)
        assert visible_table is not None
        for title in STATUS_HISTORY_HEADER_TITLES:
            th = visible_table.find_element(
                By.XPATH, f'.//thead//th[contains(text(),"{title}")]'
            )
            assert th.is_displayed()
