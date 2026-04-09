"""
Dispatch - dispatch map tests.

Validates drag-and-drop order reassignment between routes, and
verifies that map filters, route box, and region selectors work
correctly on the Dispatch Map page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.dispatch_page import DispatchPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestDispatchMap:
    """
    Verify Dispatch Map functionality: drag-and-drop orders, filters, and buttons.

    Usage:
        pytest tests/web/dispatch/test_dispatch_map.py -v
    """

    def _open_dispatch_map(self, driver):
        """Navigate to the Dispatch Map page."""
        page = DispatchPage(driver)
        page.navigate_to_dispatch_map()
        return page

    def test_c59656_drag_and_drop_orders_from_routes(self, driver):
        """C59656 Drag and drop orders from routes."""
        page = self._open_dispatch_map(driver)

        # Click Load Dispatch Grid
        page.click_load_dispatch_grid()

        # Wait for accordion to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "leftPanelAccordionContainer"))
        )

        # Expand first route panel (expandicon_101)
        page.expand_route_panel(0, "expandicon_101")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-counter="1201"]'))
        )

        # Expand second route panel (expandicon_102)
        page.expand_route_panel(1, "expandicon_102")
        # Wait for second panel orders to load
        WebDriverWait(driver, 15).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, '[data-counter="1201"]')) >= 2
        )

        # Drag order from first route to second route
        page.drag_order_between_routes("1201")

        # Wait for page to settle after drag-and-drop
        wait_for_loading_screen(driver)

    def test_c67610_filters_and_buttons_are_working(self, driver):
        """C67610 Filters and buttons are working."""
        page = self._open_dispatch_map(driver)

        # Click the search/apply button (12th li)
        page.click_map_search()

        # Expand route 101
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#expandicon_101 svg.svg-plus-icon")
            )
        ).click()

        # Open route box and select region
        page.click_element(*page.ROUTE_BOX_BTN)
        page.click_element(*page.ROUTE_BOX_PANEL_SELECT_REGION)

        # Select first route filter checkbox
        page.click_element(*page.RIGHT_PANEL_ROUTE_FILTER_FIRST)

        # Open region filter and check WA
        page.click_element(*page.REGION_FILTER_ARROW)

        wa_checkbox = page.find_clickable(*page.WA_CHECKBOX)
        if not wa_checkbox.is_selected():
            wa_checkbox.click()

        # Click search again
        page.click_map_search()

        # Expand route 102
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#expandicon_102 svg.svg-plus-icon")
            )
        ).click()

        wait_for_loading_screen(driver)
