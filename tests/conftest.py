import time
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers.app_driver import create_driver
from config.settings import SPLASH_WAIT


PERMISSION_ALLOW_IDS = [
    "com.android.permissioncontroller:id/permission_allow_button",
    "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
    "com.android.packageinstaller:id/permission_allow_button",
]


def dismiss_all_permissions(driver, max_popups=5):
    """Dismiss any Android permission pop-ups by tapping Allow."""
    for _ in range(max_popups):
        dismissed = False
        for btn_id in PERMISSION_ALLOW_IDS:
            try:
                btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((AppiumBy.ID, btn_id))
                )
                btn.click()
                dismissed = True
                time.sleep(0.5)
                break
            except Exception:
                continue
        if not dismissed:
            break


@pytest.fixture(scope="session")
def driver():
    """
    Pytest fixture to initialize Appium driver once for the entire test session.
    Waits for splash screen and dismisses permission pop-ups before yielding.
    """
    driver = create_driver()

    # Wait for splash screen to finish
    time.sleep(SPLASH_WAIT)

    # Dismiss any permission pop-ups that appear after splash
    dismiss_all_permissions(driver)

    yield driver
    driver.quit()
