"""
Routes - route log tests.

Validates that the Route Log page displays correctly with the
expected page title, visible data table, and populated data rows.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.routes_page import RoutesPage
from helpers.web_helper import navigate_to_menu, wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestRouteLog:
    """
    Verify Route Log page display and data.

    Usage:
        pytest tests/web/routes/test_route_log.py -v
    """

    def test_c67609_route_log_page_display_and_data(self, driver):
        """C67609 Verify Route Log page displays correctly with data."""
        # Navigate to Operations > Route Log
        navigate_to_menu(driver, "Operations")
        routes_page = RoutesPage(driver)
        routes_page.open_route_log()

        # Verify page title
        page_title = routes_page.get_page_title()
        assert "Route Log" in page_title or "Route" in page_title, (
            f"Page title should contain 'Route Log', got '{page_title}'"
        )

        # Verify data grid / table is visible
        table_visible = routes_page.element_is_visible(
            *routes_page.ROUTE_LOG_TABLE, timeout=10
        ) or routes_page.is_data_grid_visible()

        assert table_visible, (
            "Route Log table should be visible on the page"
        )

        # Verify data rows exist
        row_count = routes_page.get_data_row_count()
        assert row_count > 0, (
            f"Route Log should contain data rows, found {row_count}"
        )
