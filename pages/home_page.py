from .base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class HomePage(BasePage):
    """
    Page object for Home screen (Routes screen), post-login.
    """

    # Locators
    ROUTE_TITLE_XPATH = '//android.widget.TextView[@resource-id="com.allymobile_jates:id/tvTitle" and @text="Routes"]'
    DATE_ID = "com.allymobile_jates:id/tvTitleDate"
    ROUTE_LIST_SCROLL_ID = "com.allymobile_jates:id/garae_scroll"

    def is_displayed(self):
        """Return True if the Routes title is visible on the home screen."""
        try:
            element = self.find_element(AppiumBy.XPATH, self.ROUTE_TITLE_XPATH)
            return element is not None
        except Exception:
            return False

    def get_route_title_text(self):
        """Return the text of the Routes title element."""
        element = self.find_element(AppiumBy.XPATH, self.ROUTE_TITLE_XPATH)
        return element.text

    def get_date_text(self):
        """Return the text of the date element."""
        element = self.find_element(AppiumBy.ID, self.DATE_ID)
        return element.text

    def is_route_list_displayed(self):
        """Return True if the route list ScrollView is present."""
        try:
            element = self.find_element(AppiumBy.ID, self.ROUTE_LIST_SCROLL_ID)
            return element is not None
        except Exception:
            return False

    def get_route_names(self):
        """Return a list of route name strings from the route list."""
        elements = self.driver.find_elements(AppiumBy.ID, "com.allymobile_jates:id/tvTitle")
        return [el.text for el in elements if el.text and el.text != "Routes"]
