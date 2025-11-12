"""
Login - Page Display tests.

"""
from datetime import datetime

import pytest

from pages.web.login_page import WebLoginPage


@pytest.mark.usefixtures("driver")
class TestLoginPageDisplay:
    """
    Verify login page UI elements, logos, EULA display, and icons.

    Usage:
        pytest tests/web/test_00_login/test_01_login_page_display.py -v
    """

    def test_c70028_elements_logo_displayed(self, driver):
        """C70028 Verify Elements Logo displays at the top of the screen."""
        login_page = WebLoginPage(driver)
        assert login_page.is_elements_logo_visible(), (
            "Elements logo should be visible at the top of the screen"
        )

    def test_c70029_login_box_logo_displayed(self, driver):
        """C70029 Routeware Elements Logo displays at the top of the login box."""
        login_page = WebLoginPage(driver)
        assert login_page.is_login_box_logo_visible(), (
            "Login box logo should be visible"
        )

    def test_c70030_title_text_displayed(self, driver):
        """C70030 Verify title 'Please enter your company, email, and password' is displayed."""
        login_page = WebLoginPage(driver)
        assert login_page.is_title_visible(), (
            "Title text should be visible on the login page"
        )

    def test_c70031_login_fields_displayed(self, driver):
        """C70031 Company, Email, and Password fields display correctly."""
        login_page = WebLoginPage(driver)

        assert login_page.is_company_field_visible(), (
            "Company field should be visible and enabled"
        )
        assert login_page.is_email_field_visible(), (
            "Email field should be visible and enabled"
        )
        assert login_page.is_password_field_visible(), (
            "Password field should be visible, enabled, and type=password"
        )

    def test_c70032_field_icons_displayed(self, driver):
        """C70032 Logo next to Company (Building), Email (Person), and Password (Lock) display correctly."""
        login_page = WebLoginPage(driver)

        assert login_page.get_icon_in_parent(
            login_page.COMPANY_FIELD, ["building", "Building"]
        ), "Company field should have a building icon"

        assert login_page.get_icon_in_parent(
            login_page.EMAIL_FIELD, ["person", "Person", "user", "User"]
        ), "Email field should have a person/user icon"

        assert login_page.get_icon_in_parent(
            login_page.PASSWORD_FIELD, ["lock", "Lock"]
        ), "Password field should have a lock icon"

    def test_c70033_login_button_displayed(self, driver):
        """C70033 Login button displays correctly."""
        login_page = WebLoginPage(driver)
        assert login_page.is_login_button_visible(), (
            "Login button should be visible and enabled"
        )

    def test_c70034_eula_text_displayed(self, driver):
        """C70034 EULA text 'By logging in' displays correctly."""
        login_page = WebLoginPage(driver)
        assert login_page.text_is_visible(login_page.EULA_TEXT), (
            "EULA agreement text should be visible"
        )

    def test_c70035_eula_popup_opens(self, driver):
        """C70035 EULA popup opens."""
        login_page = WebLoginPage(driver)
        login_page.open_eula_modal()
        assert login_page.is_eula_modal_visible(), (
            "EULA modal should be visible after clicking EULA text"
        )

    def test_c70036_eula_text_content(self, driver):
        """C70036 EULA text displays correctly."""
        login_page = WebLoginPage(driver)
        login_page.open_eula_modal()
        assert login_page.is_eula_modal_visible(), "EULA modal should be visible"

        content = login_page.get_eula_iframe_content()
        assert "END USER LICENSE AGREEMENT" in content, (
            f"Expected EULA heading but got '{content}'"
        )

    def test_c70037_eula_close_button(self, driver):
        """C70037 X button closes EULA."""
        login_page = WebLoginPage(driver)
        login_page.open_eula_modal()
        assert login_page.is_eula_modal_visible(), "EULA modal should open"

        login_page.close_eula_modal()
        assert login_page.element_not_visible(*login_page.EULA_MODAL), (
            "EULA modal should be hidden after clicking close"
        )

    def test_c70038_copyright_displayed(self, driver):
        """C70038 Verify copyright logo is displayed correctly."""
        login_page = WebLoginPage(driver)
        current_year = datetime.now().strftime("%Y")

        copyright_text = login_page.get_copyright_text()
        assert "\u00a9" in copyright_text, "Copyright symbol should be present"
        assert current_year in copyright_text, (
            f"Current year {current_year} should be in copyright text"
        )
        assert "Routeware Inc. All rights reserved" in copyright_text, (
            "Routeware copyright notice should be present"
        )
