"""
Inventory - Inventory Search tests.

Validates equipment move with yard and status selection, inventory
detail updates including equipment type changes, and adding new
equipment with serial number and tag validation.
"""
import uuid
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.inventory_page import InventoryPage
from helpers.web_helper import (
    wait_for_loading_screen,
    force_click,
    scroll_to_element,
)


# Generate unique serial and tag numbers
_unique_suffix = uuid.uuid4().hex[:8]
SERIAL_NR = f"AutoTest{_unique_suffix}12345"
TAG_NR = f"AutoTag{_unique_suffix}12345"


@pytest.mark.usefixtures("driver")
class TestInventorySearch:
    """
    Verify Inventory Search: equipment move, details updates, and add new equipment.

    Usage:
        pytest tests/web/inventory/test_inventory_search.py -v
    """

    def _navigate_to_inventory(self, driver):
        """Navigate to Inventory > Inventory Search."""
        page = InventoryPage(driver)
        page.open_inventory()
        return page

    def test_c67629_equipment_move(self, driver):
        """C67629 Equipment Move."""
        page = self._navigate_to_inventory(driver)

        wait = WebDriverWait(driver, 10)

        # Verify URL and page title
        assert "/Operations/Inventory" in driver.current_url, (
            "URL should contain /Operations/Inventory"
        )
        assert "Inventory" in page.get_page_title(), (
            "Page title should contain 'Inventory'"
        )

        # Click search
        page.click_search()

        # Click move icon on first row (svg_stroke)
        move_icon = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#EquipmentInventoryTable tr:nth-child(1) a.btn-xs svg.svg_stroke")
        ))
        driver.execute_script("arguments[0].click();", move_icon)

        # Select move type
        Select(driver.find_element(By.ID, "Manual_MoveType")).select_by_value("1")

        # Select yard
        Select(driver.find_element(
            By.CSS_SELECTOR, '[name="Manual_Yard"]'
        )).select_by_visible_text("FL South")

        # Select equipment status
        Select(driver.find_element(By.ID, "ddlEquipmentStatus")).select_by_value("54")

        # Enter detail
        detail = driver.find_element(By.ID, "Detail")
        detail.click()
        detail.clear()
        detail.send_keys("testing")

        # Save
        driver.find_element(By.ID, "btnManualEquipmentSave").click()
        wait_for_loading_screen(driver)

        # Click view icon on first row (the eye/path icon)
        view_icon = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '#EquipmentInventoryTable tr:nth-child(1) '
            'path[d="M10.4977 16.129C13.671 16.129 16.5735 13.8473 '
            '18.2077 10.044C16.5735 6.24068 13.671 3.95901 10.4977 '
            '3.95901H10.501C7.32768 3.95901 4.42518 6.24068 2.79102 '
            '10.044C4.42518 13.8473 7.32768 16.129 10.501 16.129H10.4977Z"]'
        )))
        driver.execute_script("arguments[0].click();", view_icon)

        # Click Move History tab
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#woInventoryChildLiTab_2 a.nav-link")
        )).click()

        # Validate move history shows FL South (Clean)
        history_cell = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#EquipmentMoveHistoryTable tr:nth-child(1) td:nth-child(3)")
        ))
        history_text = history_cell.text.strip()
        assert "FL South" in history_text and "Clean" in history_text, (
            f"Move history should contain 'Yard: FL South (Clean)', got '{history_text}'"
        )

        # Validate success message
        success = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Record has been updated successfully" in success.text, (
            "Should show success message for equipment move"
        )

    def test_c67630_inventory_details_updates(self, driver):
        """C67630 Inventory details updates."""
        page = self._navigate_to_inventory(driver)

        wait = WebDriverWait(driver, 10)

        # Click search
        page.click_search()

        # Click view icon on first row (i > svg.svg_stroke)
        view_icon = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#EquipmentInventoryTable tr:nth-child(1) i svg.svg_stroke")
        ))
        driver.execute_script("arguments[0].click();", view_icon)

        # Verify popup header
        assert wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#InventoryPopup_1 div:nth-child(1) > div:nth-child(1) > h2")
        )).is_displayed(), "Inventory popup header should be visible"

        # Click Details tab (tab 3)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#woInventoryChildLiTab_3 span")
        )).click()
        wait_for_loading_screen(driver)

        # Click edit equipment button
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#inverntoryBodyContent button.edit_equip_btn")
        )).click()

        # Click update equipment type
        wait.until(EC.element_to_be_clickable(
            (By.ID, "btnUpdateEquipmentType")
        )).click()
        wait_for_loading_screen(driver)

        # Validate success message
        success = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Equipment Type updated successfully" in success.text, (
            "Should show equipment type updated message"
        )

    def test_c67631_add_new_equipment(self, driver):
        """C67631 Add new equipment."""
        page = self._navigate_to_inventory(driver)

        wait = WebDriverWait(driver, 15)
        wait_for_loading_screen(driver)

        # Click Add Inventory
        page.click_add_inventory()

        # Enter serial number
        serial_field = wait.until(EC.element_to_be_clickable(
            (By.ID, "txtAddSerialNbr")
        ))
        serial_field.clear()
        serial_field.send_keys("testing")

        # Enter tag number
        tag_field = driver.find_element(By.ID, "txtAddTagNumber")
        tag_field.clear()
        tag_field.send_keys("testing")

        # Select yard
        Select(driver.find_element(
            By.CSS_SELECTOR, '[name="YardID"]'
        )).select_by_visible_text("Washington")

        # Click Registration Tracking tab
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#woChildLiTab_2 a.nav-link")
        )).click()

        # Verify registration expiration date label
        reg_label = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#RegistationTracking div:nth-child(3) > div.form-group > label.form-label")
        ))
        assert "Registration Expiration Date" in reg_label.text, (
            "Registration Expiration Date label should be present"
        )

        # Switch back to first tab
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#woChildLiTab_1 a.nav-link")
        )).click()

        # Click Save & Close without equipment type - expect error
        save_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[id="btnSave&Close"]')
        ))
        save_btn.click()

        # Verify equipment type required error
        assert wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//*[contains(text(),'Please enter Equipment Type')]"
        ))), "Should show equipment type required message"

        # Select equipment type
        Select(driver.find_element(
            By.ID, "ddlAddEquipmentType"
        )).select_by_value("AB108674-A7AE-4127-855A-EE83E1D58333")

        # Click Save & Close - expect duplicate error
        save_btn = driver.find_element(By.CSS_SELECTOR, '[id="btnSave&Close"]')
        save_btn.click()

        assert wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//*[contains(text(),'already exists. Please review and try again.')]"
        ))), "Should show duplicate serial number error"

        # Enter unique serial and tag numbers
        serial_field = driver.find_element(By.ID, "txtAddSerialNbr")
        serial_field.clear()
        serial_field.send_keys(SERIAL_NR)

        tag_field = driver.find_element(By.ID, "txtAddTagNumber")
        tag_field.clear()
        tag_field.send_keys(TAG_NR)

        # Click grouping area to dismiss any dropdowns
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#modalAddInventory div.grouping")
        )).click()

        # Click Save & Close
        save_btn = driver.find_element(By.CSS_SELECTOR, '[id="btnSave&Close"]')
        save_btn.click()

        # Validate success message
        success = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert success.is_displayed(), "Success message should be visible"
        assert "Inventory Saved Successfully" in success.text, (
            "Should show inventory saved message"
        )

        # Search for newly created equipment
        search_field = wait.until(EC.element_to_be_clickable(
            (By.ID, "txtSerialNbr")
        ))
        search_field.click()
        search_field.clear()
        search_field.send_keys(SERIAL_NR)

        page.click_search()

        # Validate equipment type column
        type_cell = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#EquipmentInventoryTable td:nth-child(3)")
        ))
        assert "AG TOWABLE" in type_cell.text, (
            f"Equipment type should contain 'AG TOWABLE', got '{type_cell.text.strip()}'"
        )
