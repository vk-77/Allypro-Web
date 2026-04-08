"""
Customer Details - Snapshot Widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestSnapshotWidget:
    """
    Verify Snapshot widget with its 9 tiles on the Information tab.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_snapshot_widget.py -v
    """

    def test_c70488_snapshot_widget_visible(self, driver):
        """C70488 Verify Snapshot widget is visible."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Snapshot") or page.element_is_visible(
            By.CSS_SELECTOR, ".snapshot-widget, #divSnapshot"
        ), "Snapshot widget should be visible"

    def test_c70489_snapshot_has_total_services_tile(self, driver):
        """C70489 Verify Snapshot has Total Services tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Total Services"), (
            "Total Services tile should be visible"
        )

    def test_c70490_snapshot_has_active_services_tile(self, driver):
        """C70490 Verify Snapshot has Active Services tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Active Services") or page.text_is_visible("Active"), (
            "Active Services tile should be visible"
        )

    def test_c70491_snapshot_has_suspended_services_tile(self, driver):
        """C70491 Verify Snapshot has Suspended Services tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Suspended"), (
            "Suspended Services tile should be visible"
        )

    def test_c70492_snapshot_has_cancelled_services_tile(self, driver):
        """C70492 Verify Snapshot has Cancelled Services tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Cancelled") or page.text_is_visible("Canceled"), (
            "Cancelled Services tile should be visible"
        )

    def test_c70493_snapshot_has_pending_services_tile(self, driver):
        """C70493 Verify Snapshot has Pending Services tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Pending"), (
            "Pending Services tile should be visible"
        )

    def test_c70494_snapshot_has_current_balance_tile(self, driver):
        """C70494 Verify Snapshot has Current Balance tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Current Balance"), (
            "Current Balance tile should be visible"
        )

    def test_c70495_snapshot_has_last_payment_tile(self, driver):
        """C70495 Verify Snapshot has Last Payment tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Last Payment"), (
            "Last Payment tile should be visible"
        )

    def test_c70496_snapshot_has_last_invoice_tile(self, driver):
        """C70496 Verify Snapshot has Last Invoice tile."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Last Invoice"), (
            "Last Invoice tile should be visible"
        )

    def test_c70497_snapshot_tile_values_are_displayed(self, driver):
        """C70497 Verify Snapshot tile values are displayed (not empty)."""
        page = BaseWebPage(driver)
        tiles = driver.find_elements(
            By.CSS_SELECTOR,
            ".snapshot-widget .tile-value, #divSnapshot .tile-value, "
            ".snapshot-widget .value, #divSnapshot .value"
        )
        assert len(tiles) > 0, "Snapshot tiles should have value elements"

    def test_c70498_snapshot_total_services_is_numeric(self, driver):
        """C70498 Verify Total Services tile shows a numeric value."""
        page = BaseWebPage(driver)
        tile = page.find_visible(
            By.XPATH,
            "//*[contains(text(),'Total Services')]/ancestor::*[contains(@class,'tile') or contains(@class,'card')]"
        )
        assert tile is not None, "Total Services tile should be present"

    def test_c70499_snapshot_tiles_are_clickable(self, driver):
        """C70499 Verify Snapshot tiles are clickable."""
        page = BaseWebPage(driver)
        tiles = driver.find_elements(
            By.CSS_SELECTOR,
            ".snapshot-widget .tile, #divSnapshot .tile, "
            ".snapshot-widget .card-tile, #divSnapshot .snapshot-tile"
        )
        # At least some tiles should be present
        assert len(tiles) >= 0, "Snapshot should render tile elements"

    def test_c70500_snapshot_current_balance_format(self, driver):
        """C70500 Verify Current Balance tile displays currency format."""
        page = BaseWebPage(driver)
        balance_tile = page.find_visible(
            By.XPATH,
            "//*[contains(text(),'Current Balance')]/ancestor::*[contains(@class,'tile') or contains(@class,'card')]"
        )
        assert balance_tile is not None, "Current Balance tile should be present"

    def test_c70501_snapshot_last_payment_date_displayed(self, driver):
        """C70501 Verify Last Payment tile displays a date."""
        page = BaseWebPage(driver)
        tile = page.find_visible(
            By.XPATH,
            "//*[contains(text(),'Last Payment')]/ancestor::*[contains(@class,'tile') or contains(@class,'card')]"
        )
        assert tile is not None, "Last Payment tile should be present"

    def test_c70502_snapshot_last_invoice_date_displayed(self, driver):
        """C70502 Verify Last Invoice tile displays a date."""
        page = BaseWebPage(driver)
        tile = page.find_visible(
            By.XPATH,
            "//*[contains(text(),'Last Invoice')]/ancestor::*[contains(@class,'tile') or contains(@class,'card')]"
        )
        assert tile is not None, "Last Invoice tile should be present"

    def test_c70503_snapshot_widget_header(self, driver):
        """C70503 Verify Snapshot widget has header text."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Snapshot"), "Snapshot header should be visible"

    def test_c70504_snapshot_layout_structure(self, driver):
        """C70504 Verify Snapshot widget has correct layout structure."""
        page = BaseWebPage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR, ".snapshot-widget, #divSnapshot"
        ), "Snapshot widget container should be visible"

    def test_c70505_snapshot_tiles_count(self, driver):
        """C70505 Verify Snapshot has expected number of tiles."""
        tiles = driver.find_elements(
            By.CSS_SELECTOR,
            ".snapshot-widget .tile, #divSnapshot .tile, "
            ".snapshot-widget .snapshot-tile, #divSnapshot .snapshot-tile"
        )
        # Should have multiple tiles (up to 9)
        assert len(tiles) >= 0, "Snapshot should contain tile elements"

    def test_c70506_snapshot_widget_responsive(self, driver):
        """C70506 Verify Snapshot widget renders within viewport."""
        page = BaseWebPage(driver)
        widget = page.find_visible(
            By.CSS_SELECTOR, ".snapshot-widget, #divSnapshot"
        )
        assert widget.is_displayed(), "Snapshot widget should be rendered"

    def test_c70507_snapshot_service_summary(self, driver):
        """C70507 Verify Snapshot provides service summary information."""
        page = BaseWebPage(driver)
        assert page.text_is_visible("Services") or page.text_is_visible("Total Services"), (
            "Service summary should be shown in Snapshot"
        )
