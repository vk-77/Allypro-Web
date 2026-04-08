"""
Customer Details - Service Info dropdown: Update Routing tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from pages.web.base_web_page import BaseWebPage
from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    scroll_to_element,
)


@pytest.mark.usefixtures("driver")
class TestServiceInfoUpdateRouting:
    """
    Service Info dropdown - Update Routing tests.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_service_info_update_routing.py -v
    """

    def test_c70562_update_routing_open_validate_process(self, driver):
        """C70562 Update Routing - open modal, validate headers, select Day and Route for all rows, Process Updates, validate success."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        # Open Update Routing from hamburger menu
        page.open_service_info_update_routing()

        # Validate modal body and Effective Date
        routing_body = wait.until(
            EC.visibility_of_element_located((By.ID, "reassignRoutingPopUpBody"))
        )

        # Effective Date label and field
        labels = routing_body.find_elements(By.CSS_SELECTOR, "label.form-label")
        eff_label_found = any("Effective Date" in lbl.text for lbl in labels)
        assert eff_label_found, "Effective Date label should be visible"
        eff_date_field = routing_body.find_element(By.ID, "reassingrouteeffectivedate")
        assert eff_date_field.is_displayed(), "Effective Date field should be visible"

        # Validate table headers
        table = driver.find_element(By.ID, "EquipmentInventoryTable")
        assert table.is_displayed(), "EquipmentInventoryTable should be visible"
        headers = table.find_elements(By.CSS_SELECTOR, "thead th")
        header_texts = [h.text for h in headers]
        expected_headers = [
            "Frequency", "Start Date", "Current Route", "Current Day",
            "Current Seq.", "Time Window", "Warning", "New Day", "New Route", "New Seq"
        ]
        for expected in expected_headers:
            assert any(expected in ht for ht in header_texts), (
                f"Header '{expected}' not found in {header_texts}"
            )

        # Select Day and Route for each row
        rows = driver.find_elements(
            By.CSS_SELECTOR, '#EquipmentInventoryTable tbody tr[id^="RRTr_"]'
        )
        for index, row in enumerate(rows):
            row_id = row.get_attribute("id")
            guid = row_id.replace("RRTr_", "")

            # Select day (1-7)
            day_select = row.find_element(By.CSS_SELECTOR, "select.reassignRoutingDDlDay")
            if day_select.is_displayed():
                Select(day_select).select_by_value(str(index + 1))

            # Select Route via Select2
            container_id = f"select2-DDlRouteRR_{guid}-container"
            try:
                container = driver.find_element(By.ID, container_id)
                if container.is_displayed():
                    scroll_to_element(driver, container)
                    driver.execute_script("arguments[0].click();", container)
                    try:
                        search_field = WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((
                                By.CSS_SELECTOR,
                                ".select2-container--open input.select2-search__field"
                            ))
                        )
                        search_field.clear()
                        search_field.send_keys("Automation test 2")
                        search_field.send_keys(Keys.ENTER)
                    except Exception:
                        options = driver.find_elements(
                            By.CSS_SELECTOR,
                            ".select2-container--open .select2-results__option"
                        )
                        for opt in options:
                            if "Automation test 2" in opt.text:
                                opt.click()
                                break
            except NoSuchElementException:
                pass

        # Click Process Updates
        process_btn = routing_body.find_element(
            By.CSS_SELECTOR, 'input[type="button"][value="Process Updates"]'
        )
        assert process_btn.is_displayed()
        process_btn.click()
        wait_for_loading_screen(driver)

        # Validate success message
        success_msg = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//*[contains(text(),'Record has been updated successfully')]"
            ))
        )
        assert success_msg.is_displayed()
