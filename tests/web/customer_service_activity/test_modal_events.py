"""
Customer Details - Service Activity work order Events tab tests.

Validates the event log table visibility and column headers (Event ID,
Date/Time, User, Type, Order Action, Location, Text, Number).
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT


EVENTS_HEADER_TITLES = [
    "Event ID", "Date/Time", "User", "Type", "Order Action",
    "Location", "Text", "Number",
]


def _open_events_tab(driver):
    """Open today's work order and activate the Events tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_EVENTS, page.WO_PANE_EVENTS)
    return page


@pytest.mark.usefixtures("driver")
class TestModalEvents:
    """
    Service Activity tab - work order Events tab.

    """

    def test_c339637_events_tab_table_visible(self, driver):
        """C339637 Events tab: Verify event log table is visible."""
        page = _open_events_tab(driver)
        pane = page.find_visible(*page.WO_PANE_EVENTS, timeout=15)
        assert "active" in pane.get_attribute("class")
        table = page.find_visible(*page.WO_EVENTS_TABLE, timeout=10)
        assert table.is_displayed()

    def test_c339638_events_tab_table_headers(self, driver):
        """C339638 Events tab: Verify table headers are present."""
        page = _open_events_tab(driver)
        tables = driver.find_elements(*page.WO_EVENTS_TABLE)
        visible_table = next((t for t in tables if t.is_displayed()), None)
        assert visible_table is not None
        for title in EVENTS_HEADER_TITLES:
            th = visible_table.find_element(
                By.XPATH, f'.//thead//th[contains(text(),"{title}")]'
            )
            assert th.is_displayed()
        # Last header cell is blank
        ths = visible_table.find_elements(By.CSS_SELECTOR, "thead th")
        last_th = ths[-1]
        assert last_th.text.strip() == ""

    def test_c339639_events_tab_empty_state(self, driver):
        """C339639 Events tab: Verify empty-state row shows no records message."""
        page = _open_events_tab(driver)
        table = page.find_visible(*page.WO_EVENTS_TABLE, timeout=10)
        tbody = page.find_visible(*page.WO_EVENTS_TABLE_BODY, timeout=10)
        # Check for empty state message
        empty_td = driver.find_elements(
            By.CSS_SELECTOR, 'tbody.tBodyEventLogServiceHistory tr td[colspan="9"]'
        )
        if empty_td:
            visible_empty = [td for td in empty_td if td.is_displayed()]
            if visible_empty:
                assert "No record exist" in visible_empty[0].text
