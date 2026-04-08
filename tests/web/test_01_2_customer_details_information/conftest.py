"""Fixtures for Customer Details Information tests."""
import pytest
from tests.web.conftest_logged_in import logged_in_driver  # noqa: F401
from config.web_settings import BASE_URL
from helpers.web_helper import wait_for_loading_screen
from pages.web.customer_page import CustomerPage


@pytest.fixture()
def driver(logged_in_driver):
    """Navigate to Home, then open Customer Details page before each test."""
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    customer_page = CustomerPage(logged_in_driver)
    customer_page.open_customer_details_page()
    yield logged_in_driver
