"""
Fixtures for tests that require an authenticated session.

Provides a session-scoped logged-in driver and a per-test reset
that navigates back to the Home page before each test.
"""
import pytest

from config.web_settings import BASE_URL, COMPANY, USERNAME, PASSWORD
from drivers.web_driver import create_web_driver
from pages.web.login_page import LoginPage
from helpers.web_helper import wait_for_loading_screen


@pytest.fixture(scope="session")
def logged_in_driver():
    """
    Session-scoped driver that logs in once and reuses the session.
    """
    driver = create_web_driver()
    driver.get(BASE_URL)
    wait_for_loading_screen(driver)

    login_page = LoginPage(driver)
    login_page.login(COMPANY, USERNAME, PASSWORD)

    yield driver
    driver.quit()


@pytest.fixture()
def driver(logged_in_driver):
    """
    Function-scoped driver that navigates to home before each test.

    Ensures each test starts from a known state (Home page).
    """
    logged_in_driver.get(BASE_URL + "Home")
    wait_for_loading_screen(logged_in_driver)
    yield logged_in_driver
