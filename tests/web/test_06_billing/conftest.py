"""Fixtures for Billing tests."""
import pytest
from tests.web.conftest_logged_in import logged_in_driver  # noqa: F401
from config.web_settings import BASE_URL
from helpers.web_helper import wait_for_loading_screen, navigate_to_menu


@pytest.fixture()
def driver(logged_in_driver):
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    navigate_to_menu(logged_in_driver, "Billing")
    wait_for_loading_screen(logged_in_driver)
    yield logged_in_driver
