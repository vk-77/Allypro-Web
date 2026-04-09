"""Fixtures for end-to-end flow tests. Driver is already logged in."""
import pytest
from tests.web.conftest_logged_in import logged_in_driver  # noqa: F401
from config.web_settings import BASE_URL
from helpers.web_helper import wait_for_loading_screen


@pytest.fixture()
def driver(logged_in_driver):
    logged_in_driver.maximize_window()
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    yield logged_in_driver
