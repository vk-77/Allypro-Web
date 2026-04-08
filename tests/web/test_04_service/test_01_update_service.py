"""
Service - Update Service.

"""
import re

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.service_page import ServicePage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT
from data.user_data import USER_DATA


@pytest.mark.usefixtures("driver")
class TestUpdateService:
    """
    Regression tests for Update Service flow.

    Usage:
        pytest tests/web/test_04_service/test_01_update_service.py -v
    """

    def test_c59635_update_service_update(self, driver):
        """C59635 Update Service - Update."""
        service_page = ServicePage(driver)
        customer_id = USER_DATA["customer_id"]

        # Select recently viewed customer and navigate to Customer Details
        service_page.select_recently_viewed_customer(customer_id)
        wait_for_loading_screen(driver)

        # Add a new service from Customer Details
        service_page.add_new_service_from_customer_details()

        # Verify we are on Customer Details page
        service_page.verify_customer_details_title()
        wait_for_loading_screen(driver)

        # Open Update Service flow: click Services tab then Update button
        service_page.click_services_tab()
        service_page.click_update_service_button()

        # Click Next on the first update service screen
        service_page.click_next_screen_2()

        # Check for future-dated changes message
        if service_page.is_future_dated_message_visible():
            # Verify the message mentions future-dated changes
            message_text = service_page.get_future_dated_message_text()
            assert re.search(
                r"future[- ]?dated changes", message_text, re.IGNORECASE
            ), (
                f"Expected 'future-dated changes' in message, "
                f"got: {message_text}"
            )
        else:
            # No future-dated message: proceed with the update flow
            # Set day of week and route
            service_page.update_service_routing(
                day_value="3", route_search="car"
            )

            # Navigate through remaining screens
            service_page.click_next_screen_5()
            service_page.click_next_screen_6()

            # Add activity, fill type and contact, then submit
            service_page.fill_activity_and_submit(
                activity_type="CUST W/CALL", contact="0785968548"
            )

            # Verify success message
            service_page.verify_update_success()
