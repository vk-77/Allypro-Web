"""
Customer Details - Service Activity work order Equipment tab tests.

Validates Deliver Serial Numbers, Save, and Equipment History visibility
and behaviour on the Equipment tab.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT


EQUIPMENT_HISTORY_HEADER_TITLES = ["Serial Nbr", "Type", "Request Date", "Request User"]


def _open_equipment_tab(driver):
    """Open today's work order and activate the Equipment tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_EQUIPMENT, page.WO_PANE_EQUIPMENT)
    return page


@pytest.mark.usefixtures("driver")
class TestModalEquipment:
    """
    Service Activity tab - work order Equipment tab.

    """

    def test_c339633_equipment_tab_deliver_serial_save_history(self, driver):
        """C339633 Equipment tab: Verify Deliver Serial Numbers, Save, and Equipment History are visible."""
        page = _open_equipment_tab(driver)
        pane = page.find_visible(*page.WO_PANE_EQUIPMENT, timeout=15)
        assert "active" in pane.get_attribute("class")

        # Label
        label = pane.find_element(
            By.XPATH, './/label[contains(text(),"Deliver Serial Numbers")]'
        )
        assert label.is_displayed()

        # Deliver Serial input
        serial_input = page.find_visible(*page.WO_EQUIP_DELIVER_SERIAL)
        assert serial_input.is_displayed()

        # Serial search trigger
        search_trigger = page.find_visible(*page.WO_EQUIP_SERIAL_SEARCH)
        assert search_trigger.is_displayed()

        # Save button
        save_btn = page.find_visible(*page.WO_EQUIP_SAVE_BTN)
        assert save_btn.is_displayed()
        assert save_btn.is_enabled()

        # Equipment History
        history_container = page.find_visible(*page.WO_EQUIP_HISTORY_CONTAINER)
        assert "Equipment History" in history_container.text

        # History table headers
        tables = driver.find_elements(*page.WO_EQUIP_HISTORY_TABLE)
        visible_table = next((t for t in tables if t.is_displayed()), None)
        assert visible_table is not None
        for title in EQUIPMENT_HISTORY_HEADER_TITLES:
            th = visible_table.find_element(
                By.XPATH, f'.//thead//th[contains(text(),"{title}")]'
            )
            assert th.is_displayed()

    def test_c339634_equipment_tab_serial_search_opens_modal(self, driver):
        """C339634 Equipment tab: Verify serial search opens Serial Number Search modal."""
        page = _open_equipment_tab(driver)
        search_trigger = page.find_visible(*page.WO_EQUIP_SERIAL_SEARCH)
        search_trigger.click()
        wait_for_loading_screen(driver)
        # Verify Serial Number Search modal
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((
                By.XPATH,
                '//*[contains(@class,"modal-content") and contains(@class,"common")]'
                '//h4[contains(@class,"modal-title") and contains(text(),"Serial Number Search")]'
            ))
        )
        yard_filter = page.find_visible(*page.WO_SERIAL_SEARCH_YARD_FILTER)
        assert yard_filter.is_displayed()

    def test_c339635_equipment_tab_serial_search_yard_filter(self, driver):
        """C339635 Equipment tab: Verify Serial Number Search yard filter selects an option and modal closes."""
        page = _open_equipment_tab(driver)
        search_trigger = page.find_visible(*page.WO_EQUIP_SERIAL_SEARCH)
        search_trigger.click()
        wait_for_loading_screen(driver)
        # Wait for modal
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((
                By.XPATH,
                '//*[contains(@class,"modal-content") and contains(@class,"common")]'
                '//h4[contains(@class,"modal-title") and contains(text(),"Serial Number Search")]'
            ))
        )
        # Select first non-placeholder option
        yard_filter = page.find_visible(*page.WO_SERIAL_SEARCH_YARD_FILTER)
        sel = Select(yard_filter)
        non_empty = [o for o in sel.options if o.get_attribute("value")]
        assert len(non_empty) >= 1, "Yard filter should have at least one non-placeholder option"
        sel.select_by_value(non_empty[0].get_attribute("value"))
        wait_for_loading_screen(driver)
        assert yard_filter.get_attribute("value") != ""
        # Grid should exist
        grid = page.find_element(*page.WO_SERIAL_SEARCH_GRID)
        assert grid is not None
        # Close modal
        modal = driver.find_element(
            By.XPATH,
            '//h4[contains(@class,"modal-title") and contains(text(),"Serial Number Search")]'
            '/ancestor::*[contains(@class,"modal-content") and contains(@class,"common")]'
        )
        close_btn = modal.find_element(
            By.CSS_SELECTOR, 'button.closeBtn[onclick*="hideAllInventoryList"]'
        )
        close_btn.click()
        wait_for_loading_screen(driver)
        # Verify modal closed
        WebDriverWait(driver, 10).until(
            lambda d: not any(
                m.is_displayed()
                for m in d.find_elements(By.CSS_SELECTOR, "#CommonLayoutPopUpContainer.modal-content.common")
            )
        )
        # Verify equipment tab still accessible
        serial_input = page.find_visible(*page.WO_EQUIP_DELIVER_SERIAL)
        assert serial_input.is_displayed()

    def test_c339636_equipment_tab_save_button_validation(self, driver):
        """C339636 Equipment tab: Verify The Button Save is working fine."""
        page = _open_equipment_tab(driver)
        serial_input = page.find_visible(*page.WO_EQUIP_DELIVER_SERIAL)
        serial_input.clear()
        save_btn = page.find_visible(*page.WO_EQUIP_SAVE_BTN)
        save_btn.click()
        wait_for_loading_screen(driver)
        # Verify error message
        error_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, "#displayMsg #divSucessContent.alert-danger"
            ))
        )
        assert error_msg.is_displayed()
        assert "Please enter deliver serial number" in error_msg.text
