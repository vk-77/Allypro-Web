"""
Login - Blank Field Validation tests.

"""
import pytest

from data.dataload import account
from pages.web.login_page import WebLoginPage


@pytest.mark.usefixtures("driver")
class TestBlankFieldValidation:
    """
    Verify blank field validations on the login form.

    Usage:
        pytest tests/web/test_00_login/test_03_blank_field_validation.py -v
    """

    def test_c70086_blank_fields_shows_company_error(self, driver):
        """C70086 With blank info, login fails with error 'Please enter company name'."""
        login_page = WebLoginPage(driver)
        login_page.click_login()
        assert login_page.text_is_visible("Please enter company name"), (
            "Error 'Please enter company name' should be visible"
        )

    def test_c70087_only_company_shows_email_error(self, driver):
        """C70087 With only a company name, login fails with error 'Please enter email'."""
        login_page = WebLoginPage(driver)
        login_page.fill_login_form(company=account["company"])
        login_page.click_login()
        assert login_page.text_is_visible("Please enter email"), (
            "Error 'Please enter email' should be visible"
        )

    def test_c70088_company_and_email_shows_password_error(self, driver):
        """C70088 With only company and email, error 'Please enter password' is shown."""
        login_page = WebLoginPage(driver)
        login_page.fill_login_form(
            company=account["company"], email=account["username"]
        )
        login_page.click_login()
        assert login_page.text_is_visible("Please enter password"), (
            "Error 'Please enter password' should be visible"
        )

    def test_c70089_missing_company_shows_company_error(self, driver):
        """C70089 With only email/password, error 'Please enter company name' is shown."""
        login_page = WebLoginPage(driver)
        login_page.fill_login_form(
            email=account["username"], password=account["password"]
        )
        login_page.click_login()
        assert login_page.text_is_visible("Please enter company name"), (
            "Error 'Please enter company name' should be visible"
        )
