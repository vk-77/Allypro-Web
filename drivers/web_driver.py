"""
Selenium WebDriver factory for browser-based Elements testing.

Uses Selenium 4's built-in driver manager (no webdriver-manager needed).
"""
from selenium import webdriver

from config.web_settings import (
    BROWSER,
    HEADLESS,
    PAGE_LOAD_TIMEOUT,
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
)


def create_web_driver():
    """
    Create and return a Selenium WebDriver configured for browser testing.

    Returns:
        selenium.webdriver instance (Chrome, Edge, or Firefox)
    """
    browser = BROWSER.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={VIEWPORT_WIDTH},{VIEWPORT_HEIGHT}")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={VIEWPORT_WIDTH},{VIEWPORT_HEIGHT}")
        driver = webdriver.Edge(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(0)  # Use explicit waits only
    return driver
