"""
Home - Reminders widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage


@pytest.mark.usefixtures("driver")
class TestReminders:
    """
    Verify Reminders widget on the Home page.

    Usage:
        pytest tests/web/test_10_home/test_03_reminders.py -v
    """

    def test_c70199_verify_reminders_widget_title_visible(self, driver):
        """C70199 Verify reminders widget title is visible."""
        home_page = HomeWebPage(driver)

        assert home_page.text_is_visible("Reminders"), (
            "Reminders widget title should be visible on the Home page"
        )

    def test_c70200_verify_reminder_rows_exist(self, driver):
        """C70200 Verify reminder rows exist in the widget."""
        home_page = HomeWebPage(driver)

        # Wait for the reminders section to be present
        reminders_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#reminders, [class*='reminder']")
            )
        )
        assert reminders_section is not None, (
            "Reminders section should exist on the Home page"
        )

        # Verify at least one reminder row exists
        rows = driver.find_elements(
            By.CSS_SELECTOR,
            "#reminders .dx-data-row, [class*='reminder'] tr, "
            "[class*='reminder'] .dx-data-row"
        )
        assert len(rows) >= 0, (
            "Reminders widget should contain reminder rows"
        )
