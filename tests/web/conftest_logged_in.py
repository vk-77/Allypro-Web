"""
Shared fixtures for tests that require an authenticated session.

Import this conftest in test modules that need a logged-in state.
These fixtures provide a driver already on the home page after login.
"""
import pytest

from config.web_settings import BASE_URL, COMPANY, USERNAME, PASSWORD
from drivers.web_driver import create_web_driver
from pages.web.login_page import WebLoginPage
from helpers.web_helper import wait_for_loading_screen


@pytest.fixture(scope="session")
def logged_in_driver():
    """
    Session-scoped driver that logs in once and reuses the session.

    Mirrors the Cypress cy.loginWithApiChecks() + cy.session() pattern.
    """
    driver = create_web_driver()
    driver.get(BASE_URL)
    wait_for_loading_screen(driver)

    login_page = WebLoginPage(driver)
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
