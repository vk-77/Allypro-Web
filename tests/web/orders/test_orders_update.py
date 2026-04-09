"""
Orders - orders update tests.

Validates multiple order updates for status and route, sequence
updates, and advanced filter / save template functionality on
the Orders page.
"""
import pytest
from datetime import datetime, timedelta
from faker import Faker

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    select_date_range,
    text_is_visible,
    force_click,
    scroll_to_element,
)
from config.web_settings import DEFAULT_WAIT

fake = Faker()
template_name = fake.user_name().replace(" ", "") + "12345"


@pytest.mark.usefixtures("driver")
class TestOrdersUpdate:
    """
    Regression tests for Orders Update page.

    Usage:
        pytest tests/web/orders/test_orders_update.py -v
    """

    def test_c59633_multiple_orders_update_status(self, driver):
        """C59633 Multiple Orders Update - Status."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        # Verify page loaded
        assert "/Operations" in driver.current_url
        assert "Orders" in wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".pageTitle")
        )).text

        # Select Last 7 Days date range
        date_picker = wait.until(EC.element_to_be_clickable(
            (By.ID, "startEndDate")
        ))
        date_picker.click()
        last_7_days = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Last 7 Days')]")
        ))
        last_7_days.click()

        # Click Load
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnLoadOprData")
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

        # Select first two checkboxes
        checkboxes = wait.until(lambda d: d.find_elements(
            By.CSS_SELECTOR, ".dx-checkbox-container"
        ))
        if len(checkboxes) > 2:
            checkboxes[1].click()
            checkboxes[2].click()

        # Click Status dropdown and select Skipped
        status_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[title="Status"]')
        ))
        status_btn.click()

        search_field = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="-search__field"]')
        ))
        search_field.send_keys("Skipped" + Keys.ENTER)

        # Click Update Selected Records
        update_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[onclick="UpdateSelectedRecords();"]')
        ))
        update_btn.click()
        wait_for_loading_screen(driver)

        # Verify no error and Skipped text visible
        assert not text_is_visible(
            driver, "Error occured. Please try again.", timeout=3
        )
        assert text_is_visible(driver, "Skipped")

    def test_c67605_multiple_orders_update_route(self, driver):
        """C67605 Multiple Orders Update - Route."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        # Select Last 7 Days
        date_picker = wait.until(EC.element_to_be_clickable(
            (By.ID, "startEndDate")
        ))
        date_picker.click()
        last_7_days = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Last 7 Days')]")
        ))
        last_7_days.click()

        load_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnLoadOprData")
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

        # Select first checkbox
        checkboxes = wait.until(lambda d: d.find_elements(
            By.CSS_SELECTOR, ".dx-checkbox-container"
        ))
        if len(checkboxes) > 1:
            checkboxes[1].click()

        # Click Route dropdown and select Car
        route_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[title="Route"]')
        ))
        route_btn.click()

        search_field = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="-search__field"]')
        ))
        search_field.send_keys("Car" + Keys.ENTER)

        # Click Update
        update_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[onclick="UpdateSelectedRecords();"]')
        ))
        update_btn.click()
        wait_for_loading_screen(driver)

        # Verify no error
        assert not text_is_visible(
            driver, "Error occured. Please try again.", timeout=3
        )

    def test_c67606_sequence_update(self, driver):
        """C67606 Sequence Update."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        wait_for_loading_screen(driver)

        # Set date range to previous month
        now = datetime.now()
        first_of_prev = now.replace(day=1) - timedelta(days=1)
        first_of_prev = first_of_prev.replace(day=1)
        last_of_prev = now.replace(day=1) - timedelta(days=1)
        from_str = first_of_prev.strftime("%m/%d/%Y")
        to_str = last_of_prev.strftime("%m/%d/%Y")

        select_date_range(driver, "txtFromDate", "txtToDate", from_str, to_str)

        # Sync daterangepicker widget via JS
        driver.execute_script("""
            var $el = jQuery('#startEndDate');
            if ($el.length) {
                var picker = $el.data('daterangepicker');
                if (picker && picker.setStartDate) {
                    picker.setStartDate(arguments[0]);
                    picker.setEndDate(arguments[1]);
                    $el.val(arguments[0] + ' - ' + arguments[1]);
                }
            }
        """, from_str, to_str)

        load_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnLoadOprData")
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

        # Select Sequence Update template via Select2
        select2_container = wait.until(EC.visibility_of_element_located(
            (By.ID, "select2-ddlTemplate2-container")
        ))
        select2_container.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".select2-container--open")
        ))
        search_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[class*="-search__field"]')
            )
        )
        search_field.clear()
        search_field.send_keys("Seq" + Keys.ENTER)
        wait_for_loading_screen(driver)

        # Reload data
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnLoadOprData")
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

        # Scroll grid right to find sequence input
        scrollable = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[class="dx-scrollable-wrapper"]')
        ))
        driver.execute_script(
            "arguments[0].querySelector('.dx-scrollable-container')"
            ".scrollLeft = 9999;",
            scrollable,
        )

        # Update first sequence field
        seq_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '[oninput="ValidateNewSeq(event,this)"]')
        ))
        driver.execute_script("arguments[0].value = '';", seq_input)
        seq_input.send_keys("2")

        # Click Save
        save_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divDisplaySequenceOptions button.btn-primary")
        ))
        save_btn.click()

        # Verify success
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Record(s) has been updated successfully." in success_msg.text

    def test_c67607_filters_advance_filter_save_template(self, driver):
        """C67607 Filters + Advance Filter + Save Template."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        wait_for_loading_screen(driver)

        # Click Statuses filter and select options
        status_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#content button[title="Statuses:"]')
        ))
        status_btn.click()

        status_checkbox_label = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#content li:nth-child(3) a label.checkbox")
        ))
        status_checkbox_label.click()

        checkbox_15 = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#content input[value="15"]')
        ))
        if not checkbox_15.is_selected():
            checkbox_15.click()

        # Click outside to close dropdown
        header = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#content div.title-header > div.p-3.mb-3.pageTopHeader-Outer "
             "> div.align-items-end.gap-2")
        ))
        header.click()

        # Toggle priorities
        priorities_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#content button[title="Priorities:"]')
        ))
        priorities_btn.click()
        priorities_btn.click()

        # Open advanced filter
        filter_label = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#FilterLabel svg.svg_stroke")
        ))
        filter_label.click()

        # Select route filter
        route_label = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '#dispatchfilterContent label[title="Carlsbad"]')
        ))
        route_label.click()

        carlsbad_checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#dispatchfilterContent input[value="Carlsbad"]')
        ))
        if not carlsbad_checkbox.is_selected():
            carlsbad_checkbox.click()

        equip_checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#dispatchfilterContent input[value="20YDRO"]')
        ))
        if not equip_checkbox.is_selected():
            equip_checkbox.click()

        # Uncheck first workflow checkbox
        workflow_checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#dispatchfilterContent li:nth-child(1) "
             "input.workflowCode_checkbox")
        ))
        if workflow_checkbox.is_selected():
            workflow_checkbox.click()

        # Enter template name and save
        template_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[name="TemplateName"]')
        ))
        template_field.click()
        template_field.send_keys(template_name)

        save_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnTemplateSave")
        ))
        save_btn.click()

        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Template Saved Successfully." in success_msg.text

        # Select saved template from filter dropdown
        filter_select = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[title="Select Filter"]')
        ))
        filter_select.click()

        search_field = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[class*="-search__field"]')
        ))
        search_field.send_keys(template_name + Keys.ENTER)

        # Load with template
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnLoadOprData")
        ))
        load_btn.click()
        wait_for_loading_screen(driver)
