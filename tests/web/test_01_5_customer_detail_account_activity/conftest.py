"""Fixtures for Customer Details > Account Activity tab tests."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.web.conftest_logged_in import logged_in_driver  # noqa: F401
from config.web_settings import BASE_URL
from helpers.web_helper import wait_for_loading_screen
from pages.web.customer_page import CustomerPage


@pytest.fixture()
def driver(logged_in_driver):
    """Navigate to Home, open Customer Details, then switch to Account Activity tab.

    Mirrors the Cypress beforeEach:
      - loginWithApiChecks (session-scoped via logged_in_driver)
      - loadCustomerDetailsFromUserData('customerId')
      - openCustomerDetailsAccountActivityTab()
      - wait for #FilterOpen to exist
      - waitForLoadingScreen
    """
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)

    customer_page = CustomerPage(logged_in_driver)
    customer_page.open_customer_details_page()
    customer_page.open_account_activity_tab()

    # Wait for the filter toolbar to be ready
    WebDriverWait(logged_in_driver, 15).until(
        EC.presence_of_element_located((By.ID, "FilterOpen"))
    )
    wait_for_loading_screen(logged_in_driver)

    yield logged_in_driver
