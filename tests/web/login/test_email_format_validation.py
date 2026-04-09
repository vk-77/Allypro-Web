"""
Login page email format validation tests.

Verifies that malformed email addresses (missing @, missing dot,
special characters) are rejected with a "Please enter valid email" error.
"""
import pytest

from data.dataload import account
from pages.web.login_page import LoginPage


@pytest.mark.usefixtures("driver")
class TestEmailFormatValidation:
    """
    Verify email format validation on the login form.

    Usage:
        pytest tests/web/login/test_email_format_validation.py -v
    """

    @pytest.mark.parametrize(
        "test_id, email, description",
        [
            (
                "C70090",
                "invalidemailcom",
                "email missing @ sign and period",
            ),
            (
                "C70091",
                "invalidemail.com",
                "email missing just the @ sign",
            ),
            (
                "C70092",
                "invalid@emailcom",
                "email missing period after @ sign",
            ),
            (
                "C70093",
                "invalid!@#$%email.com",
                "email with special characters",
            ),
        ],
        ids=["C70090-no-at-no-dot", "C70091-no-at", "C70092-no-dot", "C70093-special-chars"],
    )
    def test_invalid_email_format(self, driver, test_id, email, description):
        """Parameterized email format validation: {description}."""
        login_page = LoginPage(driver)
        login_page.attempt_login(account["company"], email, account["password"])
        assert login_page.text_is_visible("Please enter valid email."), (
            f"{test_id}: 'Please enter valid email.' should be visible for {description}"
        )
