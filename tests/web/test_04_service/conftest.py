"""Fixtures for Service tests."""
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
    """Function-scoped driver starting at Home page."""
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    yield logged_in_driver


@pytest.fixture()
def reassign_driver(logged_in_driver):
    """
    Function-scoped driver that navigates to Operations > Reassign Services.
    Mirrors Cypress beforeEach: Operations menu click + #Active_25 click.
    """
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    navigate_to_menu(logged_in_driver, "Operations")
    click_submenu(logged_in_driver, "Active_25")
    wait_for_loading_screen(logged_in_driver)
    yield logged_in_driver
