"""
Service - reassign services tests.

Validates reassigning services with route and day selection, updating
sequence numbers, and processing the reassignment with confirmation.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.service_page import ServicePage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT


@pytest.mark.usefixtures("reassign_driver")
class TestReassignService:
    """
    Regression tests for Reassign Services page.

    Usage:
        pytest tests/web/service/test_reassign_service.py -v
    """

    def test_c67609_update_sequence_day(self, reassign_driver):
        """C67609 Update Sequence day."""
        driver = reassign_driver
        service_page = ServicePage(driver)

        # Verify Reassign Services page loaded
        service_page.verify_reassign_page()

        # Open filter panel via path icon
        service_page.click_filter_label_path()

        # Select route "Automation test 1" and check its checkbox
        service_page.select_route_by_text("Automation test 1")

        # Click first frequency label and check first frequency input
        service_page.click_frequency_first_label()
        service_page.check_frequency_first_input()

        # Close filter panel
        service_page.close_filter_panel()

        # Click Load button
        service_page.click_load_button()

        # Check Update Sequence Only
        service_page.check_update_sequence_only()

        # Type sequence value in first enabled sequence field
        service_page.type_sequence_in_first_enabled("24")

        # Click Process Update
        service_page.click_process_update()

        # Verify confirmation modal
        service_page.verify_confirmation_modal()

        # Confirm process
        service_page.click_confirm_process()

        # Verify success message
        service_page.verify_success_message()

    def test_c67608_reassign_services_is_working(self, reassign_driver):
        """C67608 Reassign Services is working."""
        driver = reassign_driver
        service_page = ServicePage(driver)

        # Verify Reassign Services page loaded
        service_page.verify_reassign_page()

        # Open filter panel
        service_page.open_filter_panel()

        # Select route by label index and check CARLSBAD checkbox
        service_page.select_route_label_by_index(2)
        service_page.check_route_checkbox_by_value("CARLSBAD")

        # Click first frequency label and check X001 frequency
        service_page.click_frequency_first_label()
        service_page.check_frequency_by_value("X001")
        wait_for_loading_screen(driver)

        # Close filter panel
        service_page.close_filter_panel()

        # Click Load button
        service_page.click_load_button()
        wait_for_loading_screen(driver)

        # Select day in first enabled day dropdown (index 2)
        service_page.select_day_in_first_enabled(index=2)
        wait_for_loading_screen(driver)

        # Check reassign status checkbox (second enabled one)
        service_page.check_reassign_status_checkbox(eq_index=1)

        # Select day and route in top reassign bar
        service_page.select_top_day_route(day_value="2", route_search="car")

        # Click Apply day/route
        service_page.click_apply_day_route()

        # Click Process Update
        service_page.click_process_update()
        wait_for_loading_screen(driver)

        # Verify confirmation modal
        service_page.verify_confirmation_modal()

        # Confirm the process update is visible and click it
        confirm_btn = service_page.find_visible(
            By.ID, "btnReassignProcessUpdate", timeout=10
        )
        assert confirm_btn.is_displayed()
        confirm_btn.click()
        wait_for_loading_screen(driver)

        # Verify success message
        service_page.verify_success_message()
