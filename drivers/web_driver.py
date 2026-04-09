"""
WebDriver factory. Returns a configured Chrome, Edge, or Firefox instance.

Chrome and Edge are launched with preferences that suppress password-manager
prompts, credential-leak warnings ("Change your password"), and other
security popups that interfere with automated test runs.
"""
from selenium import webdriver

from config.web_settings import (
    BROWSER,
    HEADLESS,
    PAGE_LOAD_TIMEOUT,
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
)

# Chrome/Edge preferences that disable password-related popups
_CHROMIUM_PREFS = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False,
    "profile.default_content_setting_values.notifications": 2,
}


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
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-default-apps")
        options.add_argument("--no-first-run")
        options.add_experimental_option("prefs", _CHROMIUM_PREFS)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={VIEWPORT_WIDTH},{VIEWPORT_HEIGHT}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--no-first-run")
        options.add_experimental_option("prefs", _CHROMIUM_PREFS)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Edge(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("--headless")
        # Firefox: disable password manager and breach alerts
        options.set_preference("signon.rememberSignons", False)
        options.set_preference("signon.autofillForms", False)
        options.set_preference(
            "signon.management.page.breach-alerts.enabled", False
        )
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.implicitly_wait(0)  # Use explicit waits only
    return driver
