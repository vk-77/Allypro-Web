from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
import time

# Desired capabilities
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "moto g51 5G"   # Use device name from adb devices
options.automation_name = "UiAutomator2"

# If using a pre-installed app
options.app_package = "com.android.settings"
options.app_activity = ".Settings"

# OR if using your APK
# options.app = r"C:\path\to\your\app.apk"

# Connect to Appium server
driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4723",
    options=options
)

time.sleep(5)
