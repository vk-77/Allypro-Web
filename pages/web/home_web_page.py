"""
Page object for the Elements web Home / Dashboard screen (post-login).
"""
from selenium.webdriver.common.by import By

from .base_web_page import BaseWebPage


class HomeWebPage(BaseWebPage):
    """
    Page object for the Home page displayed after successful login.
    """

    # ── Locators ──────────────────────────────────────────────────

    PAGE_TITLE = (By.CSS_SELECTOR, "p.pageTitle")
    USER_INFO_BUTTON = (
        By.CSS_SELECTOR,
        '[data-original-title="User Info"], '
        '[title="User Info"], '
        '[data-bs-original-title="User Info"], '
        'a[href*="UserPreference"], '
        '.user-info-btn',
    )
    USER_SIDEBAR = (By.ID, "mySidebaruser")

    # ── Assertions / queries ──────────────────────────────────────

    def is_home_page_displayed(self):
        """Return True if the Home page title is visible."""
        return self.element_is_visible(*self.PAGE_TITLE)

    def get_page_title_text(self):
        """Return the page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def is_url_home(self):
        """Return True if current URL includes /Home."""
        return "/Home" in self.current_url()

    def open_user_info(self):
        """Click the User Info button to open the sidebar."""
        self.click_element(*self.USER_INFO_BUTTON)
        self.wait_for_loading_screen()

    def is_user_sidebar_visible(self):
        """Return True if the user sidebar is visible."""
        return self.element_is_visible(*self.USER_SIDEBAR)

    def get_user_sidebar_text(self):
        """Return the full text content of the user sidebar."""
        return self.get_text(*self.USER_SIDEBAR)
