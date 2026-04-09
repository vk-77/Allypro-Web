"""
Customer Details - Account Activity toolbar filter tests.

Validates Show Open toggle, Load/Clear filter buttons, and date-range
filter controls on the Account Activity tab.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen, force_click
from data.user_data import USER_DATA


ACCOUNT_ACTIVITY_CONTAINER = "#parentTabContainer_4"
LOAD_BTN = f'{ACCOUNT_ACTIVITY_CONTAINER} a.btn-primary.load_btn[onclick*="SearchWithActivityFilter"]'
CLEAR_BTN = f'{ACCOUNT_ACTIVITY_CONTAINER} button.clear_btn[onclick="ClearFilterData()"]'


@pytest.mark.usefixtures("driver")
class TestAccountActivityFilters:
    """Account Activity toolbar filter tests.

    Usage:
        pytest tests/web/customer_account_activity/test_filters.py -v
    """

    # ------------------------------------------------------------------
    # C346303 - Show Open toggle
    # ------------------------------------------------------------------
    def test_c346303_show_open_toggle_enables_and_reloads(self, driver):
        """C346303 Show Open toggle enables and triggers activity list reload."""
        page = BasePage(driver)
        wait = WebDriverWait(driver, 15)

        filter_open = driver.find_element(By.ID, "FilterOpen")
        assert not filter_open.is_selected(), "FilterOpen should start unchecked"

        driver.execute_script("arguments[0].click();", filter_open)
        assert filter_open.is_selected(), "FilterOpen should be checked after click"

        wait_for_loading_screen(driver)

    # ------------------------------------------------------------------
    # C346304 - Hide System toggle
    # ------------------------------------------------------------------
    def test_c346304_hide_system_toggle_enables_and_reloads(self, driver):
        """C346304 Hide System toggle enables and triggers activity list reload."""
        page = BasePage(driver)

        hide_system = driver.find_element(By.ID, "HideSystem")
        assert not hide_system.is_selected(), "HideSystem should start unchecked"

        driver.execute_script("arguments[0].click();", hide_system)
        assert hide_system.is_selected(), "HideSystem should be checked after click"

        wait_for_loading_screen(driver)

    # ------------------------------------------------------------------
    # C346305 - Type dropdown (Automation)
    # ------------------------------------------------------------------
    def test_c346305_type_dropdown_automation_selectable_and_load_refreshes(self, driver):
        """C346305 Type dropdown opens, Automation can be selected, and Load refreshes the grid."""
        page = BasePage(driver)
        wait = WebDriverWait(driver, 15)

        # Open the multi-select type dropdown
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        dropdown_trigger = container.find_element(By.CSS_SELECTOR, ".drpstatus dt a")
        dropdown_trigger.click()

        # Wait for the dropdown list to be visible
        type_ul = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, f"{ACCOUNT_ACTIVITY_CONTAINER} ul.typeUl"
        )))

        # Check the "Automation" checkbox
        automation_chk = driver.find_element(By.ID, "chkStatus_Automation")
        driver.execute_script("arguments[0].click();", automation_chk)
        assert automation_chk.is_selected()

        # Verify selection text shows "Automation"
        multi_sel = container.find_element(By.CSS_SELECTOR, ".multiSelstatus")
        assert "Automation" in multi_sel.text

        # Click Load
        load_btn = container.find_element(
            By.XPATH,
            ".//a[contains(@class,'btn-primary') and contains(@class,'load_btn') and contains(@onclick,'SearchWithActivityFilter') and contains(text(),'Load')]"
        )
        load_btn.click()
        wait_for_loading_screen(driver)

    # ------------------------------------------------------------------
    # C346306 - Location and customer scope dropdown
    # ------------------------------------------------------------------
    def test_c346306_location_customer_scope_dropdown_options(self, driver):
        """C346306 Location and customer scope dropdown options apply via Load."""
        page = BasePage(driver)
        wait = WebDriverWait(driver, 15)

        rows = [
            ("0", "Current Location & Customer"),
            ("1", "All Locations & Customer"),
            ("2", "Current Location"),
        ]

        # Verify option count
        select_el = driver.find_element(By.ID, "DDladdNoteFilter")
        options = select_el.find_elements(By.TAG_NAME, "option")
        assert len(options) == len(rows)

        # Verify each option label
        for value, label in rows:
            opt = select_el.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
            assert label in opt.text

        # Select each option and click Load
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        for value, _ in rows:
            Select(select_el).select_by_value(value)
            assert select_el.get_attribute("value") == value

            load_btn = container.find_element(
                By.XPATH,
                ".//a[contains(@class,'btn-primary') and contains(@class,'load_btn') and contains(@onclick,'SearchWithActivityFilter') and contains(text(),'Load')]"
            )
            load_btn.click()
            wait_for_loading_screen(driver)

    # ------------------------------------------------------------------
    # C346307 - Date range dropdown
    # ------------------------------------------------------------------
    def test_c346307_date_range_dropdown_options(self, driver):
        """C346307 Date range dropdown options apply via Load."""
        page = BasePage(driver)
        wait = WebDriverWait(driver, 15)

        rows = [
            ("-1", "Select"),
            ("0", "Past 6 months"),
            ("1", "Past Year"),
            ("2", "Past 2 Years"),
            ("3", "All"),
        ]

        select_el = driver.find_element(By.ID, "DDlDateFilter")
        options = select_el.find_elements(By.TAG_NAME, "option")
        assert len(options) == len(rows)

        for value, label in rows:
            opt = select_el.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
            assert label in opt.text

        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        for value, _ in rows:
            Select(select_el).select_by_value(value)
            assert select_el.get_attribute("value") == value

            load_btn = container.find_element(
                By.XPATH,
                ".//a[contains(@class,'btn-primary') and contains(@class,'load_btn') and contains(@onclick,'SearchWithActivityFilter') and contains(text(),'Load')]"
            )
            load_btn.click()
            wait_for_loading_screen(driver)

    # ------------------------------------------------------------------
    # C346308 - Clear button
    # ------------------------------------------------------------------
    def test_c346308_clear_button_resets_filters_to_defaults(self, driver):
        """C346308 Clear button resets filters, type selection, and search to defaults."""
        page = BasePage(driver)
        wait = WebDriverWait(driver, 15)

        # Set various filters
        filter_open = driver.find_element(By.ID, "FilterOpen")
        driver.execute_script("arguments[0].click();", filter_open)

        hide_system = driver.find_element(By.ID, "HideSystem")
        driver.execute_script("arguments[0].click();", hide_system)

        search_input = driver.find_element(By.ID, "txtsearchActivity")
        search_input.clear()
        search_input.send_keys("clear-test")

        Select(driver.find_element(By.ID, "DDladdNoteFilter")).select_by_value("1")
        assert driver.find_element(By.ID, "DDladdNoteFilter").get_attribute("value") == "1"

        Select(driver.find_element(By.ID, "DDlDateFilter")).select_by_value("2")
        assert driver.find_element(By.ID, "DDlDateFilter").get_attribute("value") == "2"

        # Open type dropdown and check first option
        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        container.find_element(By.CSS_SELECTOR, ".drpstatus dt a").click()
        first_chk = container.find_element(By.CSS_SELECTOR, "input.chkStatus")
        driver.execute_script("arguments[0].click();", first_chk)

        multi_sel_spans = container.find_elements(By.CSS_SELECTOR, ".multiSelstatus span")
        assert len(multi_sel_spans) >= 1

        # Click Clear
        clear_btn = container.find_element(
            By.XPATH,
            ".//button[contains(@class,'clear_btn') and contains(@onclick,'ClearFilterData') and contains(text(),'Clear')]"
        )
        clear_btn.click()

        # Verify defaults
        assert not driver.find_element(By.ID, "FilterOpen").is_selected()
        assert not driver.find_element(By.ID, "HideSystem").is_selected()
        assert driver.find_element(By.ID, "txtsearchActivity").get_attribute("value") == ""
        assert driver.find_element(By.ID, "DDladdNoteFilter").get_attribute("value") == "0"
        assert driver.find_element(By.ID, "DDlDateFilter").get_attribute("value") == "-1"

        checked = container.find_elements(By.CSS_SELECTOR, "input.chkStatus:checked")
        assert len(checked) == 0

        multi_sel = container.find_element(By.CSS_SELECTOR, ".multiSelstatus")
        assert multi_sel.text.strip() == ""

        select_region = container.find_element(By.CSS_SELECTOR, ".hidastatus.select-region")
        assert select_region.is_displayed()

    # ------------------------------------------------------------------
    # C346309 - Load button
    # ------------------------------------------------------------------
    def test_c346309_load_button_triggers_reload(self, driver):
        """C346309 Load button triggers activity list reload."""
        page = BasePage(driver)

        container = driver.find_element(By.CSS_SELECTOR, ACCOUNT_ACTIVITY_CONTAINER)
        load_btn = container.find_element(
            By.XPATH,
            ".//a[contains(@class,'btn-primary') and contains(@class,'load_btn') and contains(@onclick,'SearchWithActivityFilter') and contains(text(),'Load')]"
        )
        load_btn.click()
        wait_for_loading_screen(driver)
