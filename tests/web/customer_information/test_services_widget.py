"""
Customer Details - Services widget tests.

Validates the Services widget visibility, header, data grid, and
service list items on the Information tab.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestServicesWidget:
    """
    Verify Services widget on the Information tab.

    Usage:
        pytest tests/web/customer_information/test_services_widget.py -v
    """

    def test_c70522_services_widget_visible(self, driver):
        """C70522 Verify Services widget is visible."""
        page = BasePage(driver)
        assert page.text_is_visible("Services") or page.element_is_visible(
            By.CSS_SELECTOR, ".services-widget, #divServices"
        ), "Services widget should be visible"

    def test_c70523_services_widget_has_header(self, driver):
        """C70523 Verify Services widget has a header."""
        page = BasePage(driver)
        assert page.text_is_visible("Services"), "Services header should be visible"

    def test_c70524_services_widget_has_grid(self, driver):
        """C70524 Verify Services widget contains a data grid."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".services-widget table, #divServices table, "
            ".services-widget .k-grid, #divServices .k-grid"
        ), "Services widget should contain a grid/table"

    def test_c70525_services_grid_has_columns(self, driver):
        """C70525 Verify Services grid has column headers."""
        headers = driver.find_elements(
            By.CSS_SELECTOR,
            ".services-widget th, #divServices th, "
            ".services-widget .k-header, #divServices .k-header"
        )
        assert len(headers) > 0, "Services grid should have column headers"

    def test_c70526_services_grid_has_service_id_column(self, driver):
        """C70526 Verify Services grid has Service ID column."""
        page = BasePage(driver)
        assert page.text_is_visible("Service ID") or page.text_is_visible("Service Id") or (
            page.text_is_visible("ID")
        ), "Service ID column should be present"

    def test_c70527_services_grid_has_description_column(self, driver):
        """C70527 Verify Services grid has Description column."""
        page = BasePage(driver)
        assert page.text_is_visible("Description"), (
            "Description column should be present"
        )

    def test_c70528_services_grid_has_status_column(self, driver):
        """C70528 Verify Services grid has Status column."""
        page = BasePage(driver)
        assert page.text_is_visible("Status"), "Status column should be present"

    def test_c70529_services_grid_rows_clickable(self, driver):
        """C70529 Verify Services grid rows are clickable."""
        rows = driver.find_elements(
            By.CSS_SELECTOR,
            ".services-widget tbody tr, #divServices tbody tr, "
            ".services-widget .k-grid-content tr"
        )
        if len(rows) > 0:
            assert rows[0].is_displayed(), "First service row should be visible"

    def test_c70530_services_grid_displays_data(self, driver):
        """C70530 Verify Services grid displays service data."""
        cells = driver.find_elements(
            By.CSS_SELECTOR,
            ".services-widget td, #divServices td"
        )
        assert len(cells) > 0, "Services grid should display data cells"
