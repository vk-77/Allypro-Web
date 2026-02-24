from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from config.settings import (
    DEVICE_UDID,
    DEVICE_NAME,
    PLATFORM_VERSION,
    APP_PACKAGE,
    APP_ACTIVITY,
    NEW_COMMAND_TIMEOUT,
    DEFAULT_WAIT,
)


def create_driver():
    """
    Create and return Appium driver configured for device and app.

    Returns:
        Appium WebDriver instance
    """
    options = AppiumOptions()
    options.set_capability("platformName", "Android")
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("deviceName", DEVICE_NAME)
    options.set_capability("udid", DEVICE_UDID)
    options.set_capability("platformVersion", PLATFORM_VERSION)
    options.set_capability("appPackage", APP_PACKAGE)
    options.set_capability("appActivity", APP_ACTIVITY)
    options.set_capability("noReset", True)
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("newCommandTimeout", NEW_COMMAND_TIMEOUT)

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    return driver


def wait_for_activity(driver, activity_name, timeout=30):
    """
    Wait until the specified activity is present.

    Args:
        driver: Appium driver instance
        activity_name (str): Activity name to wait for
        timeout (int): Max seconds to wait
    """
    WebDriverWait(driver, timeout).until(
        lambda d: activity_name in (d.current_activity or "")
    )