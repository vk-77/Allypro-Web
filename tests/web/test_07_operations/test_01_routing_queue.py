"""
Operations - Routing Queue tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.operations_page import OperationsPage
from helpers.web_helper import (
    click_submenu,
    wait_for_loading_screen,
    select2_select,
    select_dropdown_by_index,
)


@pytest.mark.usefixtures("driver")
class TestRoutingQueue:
    """
    Verify Routing Queue - add to routing workflow.

    Usage:
        pytest tests/web/test_07_operations/test_01_routing_queue.py -v
    """

    def _navigate_to_routing_queue(self, driver):
        """Navigate to Operations > Routing Queue (Active_24)."""
        ops_page = OperationsPage(driver)
        click_submenu(driver, "Active_24")
        return ops_page

    def test_c60375_routing_add_to_routing(self, driver):
        """C60375 Routing add to routing."""
        ops_page = self._navigate_to_routing_queue(driver)

        # Verify URL contains /Operations/Assignment
        assert "/Operations/Assignment" in driver.current_url, (
            "URL should contain /Operations/Assignment"
        )

        # Select first service checkbox
        wait = WebDriverWait(driver, 10)
        first_checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[name="chkSelectServiceUID"]')
        ))
        if not first_checkbox.is_selected():
            first_checkbox.click()

        # Click Route Selected button
        wait.until(EC.element_to_be_clickable(
            (By.ID, "divRouteSelected")
        )).click()

        # Verify Dispatch Routing modal is visible
        wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(text(),'Dispatch Routing: Multiple Records')]"
        )))

        # Select Day of Week (index 1)
        day_of_week = wait.until(EC.presence_of_element_located(
            (By.ID, "ddlGridDayOfWeek_1")
        ))
        Select(day_of_week).select_by_index(1)

        # Click Select Route
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[title="Select Route"]'
        ))).click()

        # Type in search field and press Enter
        search_field = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="-search__field"]')
        ))
        search_field.send_keys("a")
        search_field.send_keys(Keys.ENTER)

        # Click validate route queue button
        wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[onclick="return validateRouteQueue();"]'
        ))).click()
        wait_for_loading_screen(driver)
