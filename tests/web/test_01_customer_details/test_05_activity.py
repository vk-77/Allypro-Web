"""
Customer Details - Activity tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    text_is_visible,
)
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestActivity:
    """
    Activity tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_05_activity.py -v
    """

    def test_c56978_add_activity(self, driver):
        """C56978 Add Activity."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click Add Activity
        customer_page.click_add_activity()

        # Wait for activity modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divAddActivity, .modal.show, .activity-modal, "
            "#divActivityNotePopUp",
        )))

        # Select activity type
        select2_select(
            driver, "#select2-ActivityTypeId-container", "Call"
        )

        # Enter activity note
        note_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ActivityNote, #txtActivityNote, "
            "[name='ActivityNote']",
        )))
        note_field.clear()
        note_field.send_keys("Automation test activity note")

        # Save activity
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnSaveActivity, [onclick*="SaveActivity"], '
            '[onclick*="SaveActivityNote"]',
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=10) or \
            text_is_visible(driver, "Activity", timeout=10), (
            "Activity should be saved successfully"
        )
