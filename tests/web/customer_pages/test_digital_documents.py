"""
Customer Pages - digital documents tests.

Validates emailing a proposal document and editing a proposal by
navigating tabs and updating the status on the Digital Documents page.
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
from data.user_data import USER_DATA


@pytest.mark.usefixtures("driver")
class TestDigitalDocuments:
    """
    Regression tests for Digital Documents page.

    Usage:
        pytest tests/web/customer_pages/test_digital_documents.py -v
    """

    def test_c67601_email_action_is_working(self, driver):
        """C67601 Email Action is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        click_submenu(driver, "Active_142")

        # Click email icon on first proposal row
        email_icon = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#ProposalsList tr:nth-child(1) button:nth-child(3) svg.svg_fill")
        ))
        email_icon.click()
        wait_for_loading_screen(driver)

        # Verify email popup label is visible
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#sendCustomerProposalEmailPopUp div:nth-child(1) > label.tech-label")
        ))

        # Check email field and fill if empty
        email_field = wait.until(EC.element_to_be_clickable(
            (By.ID, "txtProposalEmailAddress")
        ))
        email_field.click()
        current_value = email_field.get_attribute("value") or ""
        if not current_value.strip():
            email_field.clear()
            driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
                "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                email_field,
                USER_DATA["email"],
            )

        # Click Send button
        send_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#sendCustomerProposalEmailPopUp button.btn")
        ))
        send_btn.click()
        wait_for_loading_screen(driver)

        # Verify success message
        success_msg = wait.until(EC.visibility_of_element_located(
            (By.ID, "divSucessContent")
        ))
        assert "Proposal email has been sent successfully!" in success_msg.text

    def test_c67602_edit_action_is_working(self, driver):
        """C67602 Edit Action is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)

        click_submenu(driver, "Active_142")

        # Click edit icon on first proposal row (force click)
        edit_icon = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "#ProposalsList tr:nth-child(1) button:nth-child(4) svg.svg_fill path")
        ))
        driver.execute_script("arguments[0].click();", edit_icon)
        wait_for_loading_screen(driver)

        # Verify view popup is visible
        wait.until(EC.visibility_of_element_located(
            (By.ID, "divViewCustomerProposal")
        ))

        # Navigate through all tabs
        for tab_id in [
            "woChildLiTab_2",
            "woChildLiTab_3",
            "woChildLiTab_4",
            "woChildLiTab_6",
            "woChildLiTab_5",
        ]:
            tab_link = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"#{tab_id} a.nav-link")
            ))
            tab_link.click()

        wait_for_loading_screen(driver)

        # Select status dropdown value "2" (Audit tab)
        status_dropdown = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.ID, "ddlAddProposalStatus")
            )
        )
        Select(status_dropdown).select_by_value("2")
        wait_for_loading_screen(driver)
