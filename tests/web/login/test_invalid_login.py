"""
Login page invalid credential tests.

Validates that various combinations of wrong company, email, and
password produce the expected "Invalid credentials" error message.
"""
import pytest

from data.dataload import account
from pages.web.login_page import LoginPage


# Test data for invalid login scenarios
INVALID_EMAIL = "Test12@gmail.com"
INVALID_COMPANY = "All"
INVALID_PASSWORD = "Test12"


@pytest.mark.usefixtures("driver")
class TestInvalidLogin:
    """
    Verify invalid login attempts show correct error messages.

    Usage:
        pytest tests/web/login/test_invalid_login.py -v
    """

    def test_c56993_invalid_password(self, driver):
        """C56993 Invalid password not working."""
        login_page = LoginPage(driver)
        login_page.attempt_login(
            account["company"], account["username"], INVALID_PASSWORD
        )
        login_page.wait_for_loading_screen()
        assert login_page.text_is_visible("Invalid credentials"), (
            "Error message 'Invalid credentials' should be visible"
        )

    def test_c56994_invalid_email(self, driver):
        """C56994 Invalid Email not working."""
        login_page = LoginPage(driver)
        login_page.attempt_login(
            account["company"], INVALID_EMAIL, account["password"]
        )
        login_page.wait_for_loading_screen()
        assert login_page.text_is_visible(
            "Invalid credentials. Please try again."
        ), "Error message should be visible for invalid email"

    def test_c56995_page_displayed_correctly(self, driver):
        """C56995 Page is correctly displayed."""
        login_page = LoginPage(driver)
        assert login_page.is_elements_logo_visible(), (
            "Elements logo should be visible"
        )
        assert login_page.text_is_visible(login_page.EULA_TEXT), (
            "EULA text should be visible"
        )

    @pytest.mark.parametrize(
        "test_id, company, email, password, description",
        [
            (
                "C70101",
                account["company"],
                INVALID_EMAIL,
                INVALID_PASSWORD,
                "Valid company, invalid email, invalid password",
            ),
            (
                "C70082",
                account["company"],
                account["username"],
                INVALID_PASSWORD,
                "Valid company, valid email, invalid password",
            ),
            (
                "C70083",
                INVALID_COMPANY,
                account["username"],
                account["password"],
                "Invalid company, valid email, valid password",
            ),
            (
                "C70084",
                INVALID_COMPANY,
                INVALID_EMAIL,
                account["password"],
                "Invalid company, invalid email, valid password",
            ),
            (
                "C70085",
                INVALID_COMPANY,
                account["username"],
                INVALID_PASSWORD,
                "Invalid company, valid email, invalid password",
            ),
        ],
        ids=[
            "C70101-all-invalid-except-company",
            "C70082-invalid-password",
            "C70083-invalid-company",
            "C70084-invalid-company-and-email",
            "C70085-invalid-company-and-password",
        ],
    )
    def test_invalid_login_scenarios(
        self, driver, test_id, company, email, password, description
    ):
        """Parameterized invalid login: {description}."""
        login_page = LoginPage(driver)
        # Ensure login form is ready before filling
        login_page.find_clickable(*login_page.COMPANY_FIELD)
        login_page.attempt_login(company, email, password)
        login_page.wait_for_loading_screen()
        # Check for any error message variant
        assert login_page.text_is_visible("Invalid credentials", timeout=15), (
            f"{test_id}: 'Invalid credentials' should be visible for: {description}"
        )
