"""Fixtures for Orders tests."""
import pytest
from tests.web.conftest_logged_in import logged_in_driver  # noqa: F401
from config.web_settings import BASE_URL
from helpers.web_helper import (
    wait_for_loading_screen,
    navigate_to_menu,
    click_submenu,
)


@pytest.fixture()
def driver(logged_in_driver):
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    navigate_to_menu(logged_in_driver, "Operations")
    click_submenu(logged_in_driver, "Active_21")
    yield logged_in_driver
