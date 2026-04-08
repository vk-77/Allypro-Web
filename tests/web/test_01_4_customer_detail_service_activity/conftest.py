"""
Fixtures for Customer Details > Service Activity tab regression tests (01.4).

Mirrors Cypress beforeEach:
  cy.setupElementsRegressionLogin()
  cy.loadCustomerAndOpenServiceActivityTab()
"""
import pytest
from tests.web.conftest_logged_in import logged_in_driver  # noqa: F401
from config.web_settings import BASE_URL
from helpers.web_helper import wait_for_loading_screen
from pages.web.customer_page import CustomerPage


@pytest.fixture()
def driver(logged_in_driver):
    """Navigate to Home, open Customer Details, then switch to Service Activity tab."""
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    customer_page = CustomerPage(logged_in_driver)
    customer_page.open_customer_details_page()
    customer_page.open_service_activity_tab()
    yield logged_in_driver
