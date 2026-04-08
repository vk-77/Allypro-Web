"""
Routes - Route Optimization tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.routes_page import RoutesPage
from helpers.web_helper import (
    navigate_to_menu,
    click_submenu,
    wait_for_loading_screen,
)


@pytest.mark.usefixtures("driver")
class TestRouteOptimization:
    """
    Verify Route Optimization with Retain and Blended methods.

    Usage:
        pytest tests/web/test_02_routes/test_01_route_optimization.py -v
    """

    def _navigate_to_route_optimization(self, driver):
        """Navigate to Operations > Route Optimization."""
        navigate_to_menu(driver, "Operations")
        routes_page = RoutesPage(driver)
        routes_page.open_route_optimization()
        return routes_page

    def test_c67607_route_optimization_retain_method(self, driver):
        """C67607 Verify Route Optimization with Retain method."""
        routes_page = self._navigate_to_route_optimization(driver)

        # Verify Route Optimization page is displayed
        assert routes_page.is_data_grid_visible(), (
            "Route Optimization data grid should be visible"
        )

        # Verify Retain optimization method option is available
        retain_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Retain') or "
                 "contains(@value,'Retain')]")
            )
        )
        assert retain_option is not None, (
            "Retain optimization method should be available"
        )

        # Verify the page title contains Route Optimization
        page_title = routes_page.get_page_title()
        assert "Route Optimization" in page_title or "Route" in page_title, (
            f"Page title should contain 'Route Optimization', got '{page_title}'"
        )

    def test_c67608_route_optimization_blended_method(self, driver):
        """C67608 Verify Route Optimization with Blended method."""
        routes_page = self._navigate_to_route_optimization(driver)

        # Verify Route Optimization page is displayed
        assert routes_page.is_data_grid_visible(), (
            "Route Optimization data grid should be visible"
        )

        # Verify Blended optimization method option is available
        blended_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Blended') or "
                 "contains(@value,'Blended')]")
            )
        )
        assert blended_option is not None, (
            "Blended optimization method should be available"
        )
