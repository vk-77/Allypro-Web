"""
Customer Details - Service Activity tab - work order Access tab.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT


RECURRING_NOTE_FIELD_LABELS = ["Access Note", "Location Note", "Service Note"]


def _open_access_tab(driver):
    """Open today's work order and activate the Access tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_ACCESS, page.WO_PANE_ACCESS)
    return page


@pytest.mark.usefixtures("driver")
class TestModalAccessTab:
    """
    Service Activity tab - work order Access tab.

    """

    def test_c339653_access_tab_start_end_time_update_success(self, driver):
        """C339653 Access tab: Verify Start Time and End Time updates show record updated success."""
        page = _open_access_tab(driver)
        pane = page.find_visible(*page.WO_PANE_ACCESS, timeout=15)
        assert "active" in pane.get_attribute("class")

        start_time = page.find_visible(*page.WO_ACCESS_START_TIME)
        start_time.click()
        start_time.clear()
        start_time.send_keys("08:00 AM")

        end_time = page.find_visible(*page.WO_ACCESS_END_TIME)
        end_time.click()
        end_time.clear()
        end_time.send_keys("11:00 AM")
        # Blur to trigger save
        driver.execute_script("arguments[0].blur();", end_time)
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()

    def test_c339654_access_tab_recurring_notes_section(self, driver):
        """C339654 Access tab: Verify Recurring Notes section shows Access, Location, and Service note fields."""
        page = _open_access_tab(driver)
        pane = page.find_visible(*page.WO_PANE_ACCESS, timeout=15)
        assert "active" in pane.get_attribute("class")

        # Find Recurring Notes section title
        section_title = pane.find_element(
            By.XPATH,
            './/*[contains(@class,"formSectionTitle") and contains(text(),"Recurring Notes")]'
        )
        assert section_title.is_displayed()

        # Find parent panel
        panel = section_title.find_element(By.XPATH, './ancestor::*[contains(@class,"panel")]')

        for label_text in RECURRING_NOTE_FIELD_LABELS:
            label = panel.find_element(
                By.XPATH, f'.//label[contains(text(),"{label_text}")]'
            )
            assert label.is_displayed()
            # Verify associated field container
            form_group = label.find_element(By.XPATH, './ancestor::*[contains(@class,"form-group")]')
            field = form_group.find_element(By.CSS_SELECTOR, ".Inner-fieldOuter")
            assert field.is_displayed()
