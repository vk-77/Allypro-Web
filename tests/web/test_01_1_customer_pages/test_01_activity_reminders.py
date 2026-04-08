"""
Customer Pages - Activity Reminders.

.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from helpers.web_helper import (
    click_submenu,
    wait_for_loading_screen,
)
from config.web_settings import DEFAULT_WAIT


@pytest.mark.usefixtures("driver")
class TestActivityReminders:
    """
    Regression tests for Activity Reminders page.

    Usage:
        pytest tests/web/test_01_1_customer_pages/test_01_activity_reminders.py -v
    """

    def test_c67596_update_existing_activity_reminder_desc(self, driver):
        """C67596 Update existing Activity Reminder description."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        # Navigate to Activity Reminders submenu
        click_submenu(driver, "Active_141")

        # Click Select2 user dropdown and select first user
        user_select2 = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content span.select2-selection")
        ))
        user_select2.click()

        user_dropdown = wait.until(EC.presence_of_element_located(
            (By.ID, "ddlUser")
        ))
        Select(user_dropdown).select_by_index(1)

        # Click Load button
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content a.btn-primary.load_btn")
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

        # Click edit icon on first reminder row
        edit_icon = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#ActivityRemindersList tr:nth-child(1) svg.svg_fill")
        ))
        edit_icon.click()

        # Clear and update description
        description = wait.until(EC.element_to_be_clickable(
            (By.ID, "Description")
        ))
        description.click()
        description.clear()
        description.send_keys("d")

        # Click outside description to trigger change
        outside_area = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#RemiderSection div:nth-child(7) div.form-group")
        ))
        outside_area.click()

        # Click Save button
        save_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#cTabActivityPopUpBody div.d-flex > input:nth-child(2)")
        ))
        save_btn.click()
        wait_for_loading_screen(driver)
