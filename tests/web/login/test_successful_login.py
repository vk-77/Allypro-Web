"""
Login page successful login tests.

Validates password masking, redirection to the Home page, user info
sidebar, supervisor login, and responsive layout across viewports.
"""
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from data.dataload import account, supervisor
from pages.web.login_page import LoginPage
from pages.web.home_web_page import HomePage


@pytest.mark.usefixtures("driver")
class TestSuccessfulLogin:
    """
    Verify successful login flows, user info, supervisor login, and responsive display.

    Usage:
        pytest tests/web/login/test_successful_login.py -v
    """

    def test_c70094_password_hidden_when_entered(self, driver):
        """C70094 Password text is hidden when entered."""
        login_page = LoginPage(driver)

        assert login_page.get_password_field_type() == "password", (
            "Password field type should be 'password' before typing"
        )
        login_page.enter_password("testpassword123")
        assert login_page.get_password_field_type() == "password", (
            "Password field type should remain 'password' after typing"
        )
        assert login_page.get_password_field_value() == "testpassword123", (
            "Password field value should match typed text"
        )

    def _login_and_wait_for_home(self, driver, company, username, password):
        """Login and wait until URL contains /Home."""
        login_page = LoginPage(driver)
        login_page.attempt_login(company, username, password)
        login_page.wait_for_loading_screen()
        # Wait for redirect to Home page
        WebDriverWait(driver, 30).until(
            lambda d: "/Home" in d.current_url
        )

    def test_c70095_user_sent_to_home_screen(self, driver):
        """C70095 User is sent to the home screen."""
        home_page = HomePage(driver)

        self._login_and_wait_for_home(
            driver, account["company"], account["username"], account["password"]
        )

        assert "Home" in home_page.get_page_title_text(), (
            "Page title should contain 'Home'"
        )
        assert home_page.is_url_home(), (
            "URL should include '/Home' after login"
        )

    def test_c70096_user_info_shows_correct_company(self, driver):
        """C70096 In User Info, company name and user are correct for credentials entered."""
        home_page = HomePage(driver)

        self._login_and_wait_for_home(
            driver, account["company"], account["username"], account["password"]
        )

        home_page.open_user_info()
        assert home_page.is_user_sidebar_visible(), (
            "User sidebar should be visible"
        )

        sidebar_text = home_page.get_user_sidebar_text()
        assert "Company" in sidebar_text, (
            "Sidebar should contain 'Company' label"
        )
        assert account["company"].upper() in sidebar_text.upper(), (
            f"Sidebar should contain company name '{account['company']}'"
        )

    def test_c70097_supervisor_login(self, driver):
        """C70097 User should be able to login as Supervisor."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        self._login_and_wait_for_home(
            driver,
            supervisor["company"],
            supervisor["username"],
            supervisor["password"],
        )

        assert "Home" in home_page.get_page_title_text(), (
            "Page title should contain 'Home' after supervisor login"
        )
        assert home_page.is_url_home(), (
            "URL should include '/Home' after supervisor login"
        )
        assert login_page.text_not_present(
            "Please enter your company, email and password"
        ), "Login form should no longer be visible"
        assert login_page.text_not_present("Invalid credentials"), (
            "No error messages should be visible after successful login"
        )

    def test_c70098_login_page_responsive(self, driver):
        """C70098 Login page displays correctly at any size."""
        login_page = LoginPage(driver)

        viewports = [
            (375, 667),
            (768, 1024),
            (1280, 1000),
            (1920, 1080),
        ]

        for width, height in viewports:
            driver.set_window_size(width, height)

            assert login_page.is_elements_logo_visible(), (
                f"Elements logo should be visible at {width}x{height}"
            )
            assert login_page.is_login_box_logo_visible(), (
                f"Login box logo should be visible at {width}x{height}"
            )
            assert login_page.is_title_visible(), (
                f"Title text should be visible at {width}x{height}"
            )
            assert login_page.is_company_field_visible(), (
                f"Company field should be visible at {width}x{height}"
            )
            assert login_page.is_email_field_visible(), (
                f"Email field should be visible at {width}x{height}"
            )
            assert login_page.is_password_field_visible(), (
                f"Password field should be visible at {width}x{height}"
            )
            assert login_page.is_login_button_visible(), (
                f"Login button should be visible at {width}x{height}"
            )
            assert login_page.text_is_visible(login_page.EULA_TEXT), (
                f"EULA text should be visible at {width}x{height}"
            )
