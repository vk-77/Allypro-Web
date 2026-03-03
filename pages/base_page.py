import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import DEFAULT_WAIT


class BasePage:
    """
    Base class with common Appium actions:
    - wait for elements
    - click elements
    - type text
    - dismiss permission pop-ups
    """
    

    # Common Android permission dialog button IDs
    PERMISSION_ALLOW_IDS = [
        "com.android.permissioncontroller:id/permission_allow_button",
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
        "com.android.packageinstaller:id/permission_allow_button",
    ]
    PERMISSION_DENY_ID = "com.android.permissioncontroller:id/permission_deny_button"

    def __init__(self, driver):
        # Initialize driver and default explicit wait
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT)

    def dismiss_permission_popups(self, action="allow", max_popups=5):
        """
        Dismiss any Android permission pop-ups that appear.

        Args:
            action: 'allow' to grant permissions, 'deny' to reject them
            max_popups: Maximum number of consecutive popups to dismiss
        """
        for _ in range(max_popups):
            dismissed = False
            if action == "allow":
                for btn_id in self.PERMISSION_ALLOW_IDS:
                    try:
                        btn = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((AppiumBy.ID, btn_id))
                        )
                        btn.click()
                        dismissed = True
                        time.sleep(0.5)
                        break
                    except Exception:
                        continue
            else:
                try:
                    btn = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((AppiumBy.ID, self.PERMISSION_DENY_ID))
                    )
                    btn.click()
                    dismissed = True
                    time.sleep(0.5)
                except Exception:
                    pass
            if not dismissed:
                break

    def find_element(self, by, value):
        """
        Wait for element presence and return it.

        Args:
            by: Locator strategy (e.g., AppiumBy.ID)
            value: Locator string

        Returns:
            WebElement when found
        """
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_clickable(self, by, value):
        """
        Wait for element to be clickable and return it.

        Args:
            by: Locator strategy
            value: Locator string

        Returns:
            WebElement when clickable
        """
        return self.wait.until(EC.element_to_be_clickable((by, value)))

    def type_text(self, resource_id, text):
        """
        Click input field, clear it, and type text.

        Args:
            resource_id: Element resource ID
            text: Text to input
        """
        try:
            field = self.find_element(AppiumBy.ID, resource_id)
            field.click()
            field.clear()
            field.send_keys(text)
        except Exception as e:
            print(f"Typing failed for {resource_id}: {e}")

    def click(self, resource_id):
        """
        Click element by resource ID.

        Args:
            resource_id: Element resource ID
        """
        try:
            btn = self.find_clickable(AppiumBy.ID, resource_id)
            btn.click()
        except Exception as e:
            print(f"Click failed for {resource_id}: {e}")