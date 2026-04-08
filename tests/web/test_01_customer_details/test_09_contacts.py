"""
Customer Details - Contacts tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    text_is_visible,
)
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestContacts:
    """
    Contact tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_09_contacts.py -v
    """

    def test_c56983_create_customer_contact(self, driver):
        """C56983 Create Customer Contact."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Contacts tab
        customer_page.open_contacts_tab()

        # Click Add Contact button
        add_contact_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnAddContact, [onclick*="AddContact"], '
            '[onclick*="ShowAddContactPopup"]',
        )))
        add_contact_btn.click()
        wait_for_loading_screen(driver)

        # Wait for contact modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divAddContact, .modal.show, .contact-modal",
        )))

        # Fill contact first name
        first_name_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ContactFirstName, #FirstName, [name='FirstName']",
        )))
        first_name_field.clear()
        first_name_field.send_keys("AutoTest")

        # Fill contact last name
        last_name_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ContactLastName, #LastName, [name='LastName']",
        )))
        last_name_field.clear()
        last_name_field.send_keys("Contact")

        # Fill email
        email_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ContactEmail, #Email, [name='Email']",
        )))
        email_field.clear()
        email_field.send_keys("autotest.contact@test.com")

        # Fill phone
        phone_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ContactPhone, #Phone, [name='Phone']",
        )))
        phone_field.clear()
        phone_field.send_keys(USER_DATA["mobile"])

        # Save contact
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnSaveContact, [onclick*="SaveContact"]',
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=10) or \
            text_is_visible(driver, "AutoTest", timeout=10), (
            "Contact should be created successfully"
        )

    def test_c56984_search_customer_contact(self, driver):
        """C56984 Search Customer Contact."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Contacts tab
        customer_page.open_contacts_tab()

        # Enter search text in contacts search field
        search_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#txtSearchContact, .contact-search input, "
            "[placeholder*='Search'], #contactSearchInput",
        )))
        search_field.clear()
        search_field.send_keys(USER_DATA["contact_name"])
        wait_for_loading_screen(driver)

        # Verify search results contain the contact
        assert text_is_visible(driver, USER_DATA["contact_name"], timeout=10), (
            f"Contact '{USER_DATA['contact_name']}' should appear in search results"
        )
