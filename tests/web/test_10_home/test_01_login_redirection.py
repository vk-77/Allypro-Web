"""
Home - Login Redirection tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage
from pages.web.login_page import WebLoginPage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import BASE_URL


@pytest.mark.usefixtures("driver")
class TestLoginRedirection:
    """
    Verify login redirects to Home page and user can log out.

    Usage:
        pytest tests/web/test_10_home/test_01_login_redirection.py -v
    """

    def test_c70106_verify_url_includes_home_and_page_title_visible(self, driver):
        """C70106 Verify URL includes /Home and page title is visible."""
        home_page = HomeWebPage(driver)

        assert "/Home" in driver.current_url, (
            "URL should include '/Home' after login"
        )
        assert home_page.is_home_page_displayed(), (
            "Home page title should be visible"
        )

    def test_c70185_verify_user_can_log_out(self, driver):
        """C70185 Verify user can log out (click user image > logout > see login page)."""
        home_page = HomeWebPage(driver)

        # Click user image to open sidebar
        home_page.open_user_info()

        # Click logout link
        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".al-userLogout a")
            )
        )
        logout_link.click()
        wait_for_loading_screen(driver)

        # Verify login page is displayed
        login_page = WebLoginPage(driver)
        assert login_page.text_is_visible(
            "Please enter your company, email and password"
        ), "Login page text should be visible after logout"
