from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess


DEVICE_UDID = "ZD22243TNC"
APP_PACKAGE = "com.allymobile_jates"


def adb_shell(cmd):
    """Run an ADB shell command on the device."""
    subprocess.run(
        ["adb", "-s", DEVICE_UDID, "shell"] + cmd,
        capture_output=True,
    )


def create_driver():
    options = AppiumOptions()
    options.set_capability("platformName", "Android")
    options.set_capability("appium:automationName", "UiAutomator2")
    options.set_capability("appium:deviceName", "moto g51 5G")
    options.set_capability("appium:udid", DEVICE_UDID)
    options.set_capability("appium:platformVersion", "12")
    options.set_capability("appium:appPackage", APP_PACKAGE)
    options.set_capability("appium:appActivity", f"{APP_PACKAGE}/.activities.SplashActivity")
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 90000)
    options.set_capability("appium:uiautomator2ServerInstallTimeout", 90000)
    options.set_capability("appium:newCommandTimeout", 300)

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options,
    )
    return driver


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


def login(driver, company, username, password):
    """Fill login fields and tap login using Appium for field focus + ADB for typing."""
    wait = WebDriverWait(driver, 10)

    fields = [
        ("com.allymobile_jates:id/etCompanyName", company, "Company name"),
        ("com.allymobile_jates:id/etUserName", username, "Username"),
        ("com.allymobile_jates:id/etPassword", password, "Password"),
    ]

    for resource_id, value, label in fields:
        field = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, resource_id))
        )
        field.click()
        time.sleep(0.5)

        # Select all text and delete it
        adb_shell(["input", "keyevent", "KEYCODE_MOVE_END"])
        time.sleep(0.2)
        # Select all (Ctrl+A equivalent)
        adb_shell(["input", "keyevent", "29", "--longpress"])
        time.sleep(0.1)
        adb_shell(["input", "keyevent", "67"])  # Delete selected
        time.sleep(0.3)

        # Type the value
        adb_shell(["input", "text", value])
        display = "****" if label == "Password" else value
        print(f"  {label}: {display}")
        time.sleep(1)

    # Press back to dismiss keyboard
    adb_shell(["input", "keyevent", "4"])
    time.sleep(1)

    # Tap Login button using Appium
    try:
        login_btn = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "com.allymobile_jates:id/btnLogin")
            )
        )
        login_btn.click()
    except Exception:
        # Fallback: use ADB tap on the login button location
        print("  Using ADB tap fallback for Login button...")
        # Get button bounds from UI dump
        result = subprocess.run(
            ["adb", "-s", DEVICE_UDID, "shell", "uiautomator", "dump", "/dev/tty"],
            capture_output=True, text=True,
        )
        import re
        match = re.search(r'resource-id="com\.allymobile_jates:id/btnLogin"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', result.stdout)
        if match:
            x = (int(match.group(1)) + int(match.group(3))) // 2
            y = (int(match.group(2)) + int(match.group(4))) // 2
            adb_shell(["input", "tap", str(x), str(y)])
        else:
            raise Exception("Could not find Login button")

    print("Login button tapped!")


def main():
    print("Starting Routeware test...")
    driver = create_driver()

    try:
        print("App launched successfully!")
        print(f"Current activity: {driver.current_activity}")

        # Wait for the splash screen to pass
        time.sleep(5)
        print(f"Activity after splash: {driver.current_activity}")

        # Handle all permission dialogs if any
        print("\nChecking for permission dialogs...")
        granted = handle_permissions(driver, timeout=5)
        if granted > 0:
            print(f"Granted {granted} permission(s).")
        else:
            print("No permission dialogs found.")

        # If app is not on login screen, relaunch it
        time.sleep(2)
        current = driver.current_activity or ""
        if "LoginActivity" not in current:
            print(f"\nCurrent activity is '{current}', relaunching app...")
            driver.activate_app(APP_PACKAGE)
            time.sleep(5)
            extra = handle_permissions(driver, timeout=3)
            if extra:
                print(f"Granted {extra} additional permission(s).")

        # Wait for login screen
        print("\nWaiting for login screen...")
        WebDriverWait(driver, 30).until(
            lambda d: "LoginActivity" in (d.current_activity or "")
        )
        print(f"On login screen! Activity: {driver.current_activity}")

        # Login
        print("\nEntering login credentials...")
        login(driver, "allypro", "vk77", "1234")

        # Wait for login to complete
        time.sleep(8)
        post_login_activity = driver.current_activity or ""
        print(f"\nPost-login activity: {post_login_activity}")

        if "LoginActivity" not in post_login_activity:
            print("Login successful!")
        else:
            print("Still on login screen - check credentials or network.")

    except Exception as e:
        print(f"Test failed: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
