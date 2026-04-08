"""
Search - Advanced Filter Search tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.search_page import SearchPage
from data.user_data import USER_DATA
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestAdvancedFilterSearch:
    """
    Verify advanced search filter functionality.

    Usage:
        pytest tests/web/test_11_search/test_05_advanced_filter_search.py -v
    """

    def _open_advanced_search(self, driver):
        """Open the advanced search panel."""
        search_page = SearchPage(driver)
        adv_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(search_page.ADVANCED_FILTER_BTN)
        )
        adv_btn.click()
        wait_for_loading_screen(driver)
        return search_page

    def test_advanced_filter_by_customer_id(self, driver):
        """Verify advanced filter search by Customer ID returns results."""
        search_page = self._open_advanced_search(driver)

        # Enter Customer ID in advanced filter
        customer_id_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_page.FILTER_CUSTOMER_ID)
        )
        customer_id_field.clear()
        customer_id_field.send_keys(USER_DATA["customer_id"])
        customer_id_field.send_keys(Keys.ENTER)
        wait_for_loading_screen(driver)

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible after filtering by Customer ID"
        )
        assert search_page.has_results(), (
            "Advanced filter by Customer ID should return results"
        )

    def test_advanced_filter_by_customer_name(self, driver):
        """Verify advanced filter search by Customer Name returns results."""
        search_page = self._open_advanced_search(driver)

        # Enter Customer Name in advanced filter
        name_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_page.FILTER_NAME)
        )
        name_field.clear()
        name_field.send_keys(USER_DATA["customer_name"])
        name_field.send_keys(Keys.ENTER)
        wait_for_loading_screen(driver)

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible after filtering by Name"
        )
        assert search_page.has_results(), (
            "Advanced filter by Customer Name should return results"
        )

    def test_advanced_filter_by_location_id(self, driver):
        """Verify advanced filter search by Location ID returns results."""
        search_page = self._open_advanced_search(driver)

        # Enter Location ID in advanced filter
        location_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_page.FILTER_LOCATION_ID)
        )
        location_field.clear()
        location_field.send_keys(USER_DATA["location_id"])
        location_field.send_keys(Keys.ENTER)
        wait_for_loading_screen(driver)

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible after filtering by Location ID"
        )
        assert search_page.has_results(), (
            "Advanced filter by Location ID should return results"
        )

    def test_advanced_filter_by_service_id(self, driver):
        """Verify advanced filter search by Service ID returns results."""
        search_page = self._open_advanced_search(driver)

        # Enter Service ID in advanced filter
        service_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_page.FILTER_SERVICE_ID)
        )
        service_field.clear()
        service_field.send_keys(USER_DATA["service_id"])
        service_field.send_keys(Keys.ENTER)
        wait_for_loading_screen(driver)

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible after filtering by Service ID"
        )
        assert search_page.has_results(), (
            "Advanced filter by Service ID should return results"
        )

    def test_advanced_filter_by_address(self, driver):
        """Verify advanced filter search by Address returns results."""
        search_page = self._open_advanced_search(driver)

        # Enter Address in advanced filter
        address_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(search_page.FILTER_ADDRESS)
        )
        address_field.clear()
        address_field.send_keys(USER_DATA["address"])
        address_field.send_keys(Keys.ENTER)
        wait_for_loading_screen(driver)

        assert search_page.is_result_grid_visible(), (
            "Search result grid should be visible after filtering by Address"
        )
        assert search_page.has_results(), (
            "Advanced filter by Address should return results"
        )
