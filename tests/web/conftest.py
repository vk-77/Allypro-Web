"""
Session-scoped WebDriver and per-test driver reset fixture.

Each test gets a clean browser state (cookies/storage cleared,
navigated to base URL) so it starts from the login page.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from drivers.web_driver import create_web_driver
from config.web_settings import BASE_URL


@pytest.fixture(scope="session")
def web_driver():
    """
    Session-scoped Selenium WebDriver.

    Creates the browser once for the entire test session and quits on teardown.
    """
    driver = create_web_driver()
    yield driver
    driver.quit()


@pytest.fixture()
def driver(web_driver):
    """
    Function-scoped driver wrapper that clears state before each test.

    Clears session storage, cookies, and navigates to the base URL so
    every test starts from a clean login page.
    """
    web_driver.delete_all_cookies()
    try:
        web_driver.execute_script(
            "window.sessionStorage.clear(); window.localStorage.clear();"
        )
    except Exception:
        pass
    web_driver.get(BASE_URL)
    # Wait for login page to be ready (Company field visible)
    try:
        WebDriverWait(web_driver, 15).until(
            EC.visibility_of_element_located((By.ID, "CompanyName"))
        )
    except Exception:
        # If we're not on the login page (e.g., already logged in), that's OK
        pass
    yield web_driver
