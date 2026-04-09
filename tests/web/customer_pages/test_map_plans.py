"""
Customer Pages - map plans tests.

Validates deleting a map plan, viewing plan details with the map
canvas, editing an existing plan, and adding a new region.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers.web_helper import (
    click_submenu,
    wait_for_loading_screen,
    text_is_visible,
)
from config.web_settings import DEFAULT_WAIT


@pytest.mark.usefixtures("driver")
class TestMapPlans:
    """
    Regression tests for Map Plans page.

    Usage:
        pytest tests/web/customer_pages/test_map_plans.py -v
    """

    def test_c67597_delete_is_working(self, driver):
        """C67597 Delete is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        click_submenu(driver, "Active_1421")

        # Click first Delete button
        delete_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[title="Delete"]')
        ))
        delete_btn.click()
        wait_for_loading_screen(driver)

        # Verify success message
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Item has been deleted successfully." in success_msg.text

    def test_c67598_plan_details_are_working(self, driver):
        """C67598 Plan Details are working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        click_submenu(driver, "Active_1421")

        # Click Plan details link (remove target to stay in same window)
        plan_details_btn = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[title="Plan details"]')
        ))
        driver.execute_script(
            "arguments[0].removeAttribute('target');", plan_details_btn
        )
        plan_details_btn.click()
        wait_for_loading_screen(driver)

        # Verify side panel heading is visible with text "PLACES"
        heading = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#mySidepanel2 h2")
        ))
        assert heading.text == "PLACES"

        # Verify map canvas is visible
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#map-canvas div.gm-style > div:nth-child(1) > div:nth-child(2)")
        ))

    def test_c67599_edit_is_working(self, driver):
        """C67599 Edit is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        click_submenu(driver, "Active_1421")

        # Click edit icon on first row
        edit_icon = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#MapPlanList tr:nth-child(1) svg.svg_fill")
        ))
        edit_icon.click()
        wait_for_loading_screen(driver)

        # Click Save button
        save_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#MapPlanContainer button.btn-primary")
        ))
        save_btn.click()
        wait_for_loading_screen(driver)

    def test_c67600_add_is_working(self, driver):
        """C67600 Add is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        click_submenu(driver, "Active_1421")

        # Click Add Region button
        add_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btn-AddRegion")
        ))
        add_btn.click()

        # Fill in Name
        name_field = wait.until(EC.element_to_be_clickable(
            (By.ID, "txtName")
        ))
        name_field.click()
        name_field.send_keys("Automation Test")

        # Fill in Description
        desc_field = wait.until(EC.element_to_be_clickable(
            (By.ID, "txtDescription")
        ))
        desc_field.click()
        desc_field.send_keys("Desc")

        # Click checkbox / toggle
        toggle = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#divMapForm div.Inner-fieldOuter > span.d-block")
        ))
        toggle.click()

        # Click Customer ID field
        cust_id = wait.until(EC.element_to_be_clickable(
            (By.ID, "txtCustID")
        ))
        cust_id.click()

        # Stub window.open to keep navigation in same tab
        driver.execute_script(
            "window.open = function(url) { window.location.href = url; };"
        )

        # Click Save
        save_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#MapPlanContainer button.btn-primary")
        ))
        save_btn.click()

        # Verify side panel visible
        wait.until(EC.visibility_of_element_located(
            (By.ID, "mySidepanel2")
        ))
