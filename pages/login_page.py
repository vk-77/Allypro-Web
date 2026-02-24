from .base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class LoginPage(BasePage):
    """
    Page object representing the Login screen.

    Fields and buttons identified by resource IDs.
    """

    # Locators for login screen elements
    COMPANY_FIELD = "com.allymobile_jates:id/etCompanyName"
    USERNAME_FIELD = "com.allymobile_jates:id/etUserName"
    PASSWORD_FIELD = "com.allymobile_jates:id/etPassword"
    LOGIN_BUTTON = "com.allymobile_jates:id/btnLogin"

    def enter_company(self, company):
        """Enter text into the Company field."""
        self.type_text(self.COMPANY_FIELD, company)

    def enter_username(self, username):
        """Enter text into the Username field."""
        self.type_text(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        """Enter text into the Password field."""
        self.type_text(self.PASSWORD_FIELD, password)

    def tap_login(self):
        """Tap the Login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, company, username, password):
        """
        Complete login flow:
        - Fill company, username, password
        - Tap Login button

        Args:
            company (str): Company name
            username (str): Username
            password (str): Password
        """
        self.dismiss_permission_popups()
        self.enter_company(company)
        self.enter_username(username)
        self.enter_password(password)
        self.driver.hide_keyboard()
        self.tap_login()

    def find_element_by_id(self, resource_id):
        """Helper to find element by resource ID."""
        return self.find_element(AppiumBy.ID, resource_id)