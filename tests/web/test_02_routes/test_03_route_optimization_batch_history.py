"""
Routes - Route Optimization Batch History tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.routes_page import RoutesPage
from helpers.web_helper import navigate_to_menu, wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestRouteOptimizationBatchHistory:
    """
    Verify Route Optimization Batch History page.

    Usage:
        pytest tests/web/test_02_routes/test_03_route_optimization_batch_history.py -v
    """

    def test_c67610_batch_history_page(self, driver):
        """C67610 Verify Batch History page displays correctly."""
        # Navigate to Operations > Route Optimization
        navigate_to_menu(driver, "Operations")
        routes_page = RoutesPage(driver)
        routes_page.open_route_optimization()

        # Click Batch History tab/button
        batch_history_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(routes_page.BATCH_HISTORY_BTN)
        )
        batch_history_btn.click()
        wait_for_loading_screen(driver)

        # Verify Batch History content is visible
        assert routes_page.text_is_visible("Batch History") or \
            routes_page.is_data_grid_visible(), (
            "Batch History page should display content"
        )

        # Verify the data grid is present
        grid_visible = routes_page.is_data_grid_visible()
        assert grid_visible, (
            "Batch History data grid should be visible"
        )
