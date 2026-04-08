"""
Search - Global Search tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.search_page import SearchPage
from pages.web.home_web_page import HomeWebPage
from data.user_data import USER_DATA
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestSearch:
    """
    Verify global search by Customer ID, Name, Location ID, Service ID,
    Address, grid columns, and result display.

    Usage:
        pytest tests/web/test_11_search/test_04_search.py -v
    """

    def test_c67640_search_by_customer_id(self, driver):
        """C67640 Verify search by Customer ID returns results."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["customer_id"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )
        assert search_page.has_results(), (
            "Search by Customer ID should return at least one result"
        )

    def test_c67641_search_by_customer_name(self, driver):
        """C67641 Verify search by Customer Name returns results."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["customer_name"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )
        assert search_page.has_results(), (
            "Search by Customer Name should return at least one result"
        )

    def test_c67642_search_by_location_id(self, driver):
        """C67642 Verify search by Location ID returns results."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["location_id"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )
        assert search_page.has_results(), (
            "Search by Location ID should return at least one result"
        )

    def test_c67643_search_by_service_id(self, driver):
        """C67643 Verify search by Service ID returns results."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["service_id"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )
        assert search_page.has_results(), (
            "Search by Service ID should return at least one result"
        )

    def test_c67644_search_by_address(self, driver):
        """C67644 Verify search by Address returns results."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["address"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )
        assert search_page.has_results(), (
            "Search by Address should return at least one result"
        )

    def test_c67645_verify_grid_columns(self, driver):
        """C67645 Verify search result grid displays expected columns."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["customer_id"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )

        # Verify expected column headers are present
        expected_columns = [
            "Customer ID", "Customer Name", "Location ID",
            "Address", "City", "State",
        ]
        for column_name in expected_columns:
            header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f"//td[contains(@class,'dx-header')] | "
                     f"//div[contains(@class,'dx-header')]"
                     f"//*[contains(text(),'{column_name}')]")
                )
            )
            assert header is not None, (
                f"Column header '{column_name}' should be present in the grid"
            )

    def test_c67646_verify_search_results_display(self, driver):
        """C67646 Verify search results are displayed correctly."""
        search_page = SearchPage(driver)

        search_page.search(USER_DATA["customer_id"])

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible"
        )
        row_count = search_page.get_result_row_count()
        assert row_count > 0, (
            f"Search should return results, but found {row_count} rows"
        )
