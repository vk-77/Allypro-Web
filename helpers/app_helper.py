import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import APP_PACKAGE


def handle_crash_dialog(driver):
    """Dismiss app crash dialog if present and relaunch the app."""
    try:
        close_btn = driver.find_element(AppiumBy.ID, "android:id/aerr_close")
        print("  App crash dialog detected - closing and relaunching...")
        close_btn.click()
        time.sleep(2)
        driver.activate_app(APP_PACKAGE)
        time.sleep(5)
        return True
    except Exception:
        return False


def handle_permissions(driver, timeout=3):
    """Handle all permission dialogs by tapping 'While using the app' or 'Allow'."""
    allow_button_ids = [
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
        "com.android.permissioncontroller:id/permission_allow_button",
        "com.android.permissioncontroller:id/permission_allow_one_time_button",
    ]
    count = 0

    while True:
        if handle_crash_dialog(driver):
            continue

        found = False
        for btn_id in allow_button_ids:
            try:
                btn = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((AppiumBy.ID, btn_id))
                )
                permission_text = driver.find_elements(
                    AppiumBy.ID,
                    "com.android.permissioncontroller:id/permission_message",
                )
                msg = permission_text[0].text if permission_text else "Unknown permission"
                print(f"  Permission requested: {msg}")
                btn.click()
                count += 1
                found = True
                time.sleep(1)
                break
            except Exception:
                continue

        if not found:
            break

    return count


def wait_for_activity(driver, activity_name, timeout=30):
    """Wait until the current activity contains the given name."""
    WebDriverWait(driver, timeout).until(
        lambda d: activity_name in (d.current_activity or "")
    )


def ensure_on_activity(driver, activity_name, timeout=30):
    """If not already on the target activity, relaunch the app and wait."""
    current = driver.current_activity or ""
    if activity_name in current:
        return

    print(f"  Current activity is '{current}', relaunching app...")
    driver.activate_app(APP_PACKAGE)
    time.sleep(5)

    extra = handle_permissions(driver, timeout=3)
    if extra:
        print(f"  Granted {extra} additional permission(s).")

    wait_for_activity(driver, activity_name, timeout)
