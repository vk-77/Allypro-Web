import time
import pytest
from config.settings import COMPANY, USERNAME, PASSWORD, POST_LOGIN_WAIT
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.usefixtures("driver")
class TestLogin:
    """
    Login flow test cases.

    Usage:
        pytest tests/test_login_flow.py
    """

    def test_login_fields_present(self, driver):
        """
        Verify all login screen fields and button are present.
        """
        login_page = LoginPage(driver)

        fields = [
            login_page.COMPANY_FIELD,
            login_page.USERNAME_FIELD,
            login_page.PASSWORD_FIELD,
            login_page.LOGIN_BUTTON,
        ]

        for resource_id in fields:
            element = login_page.find_element_by_id(resource_id)
            assert element is not None, f"Expected element {resource_id} to be present"

    def test_login_reaches_home(self, driver):
        """
        Perform login and verify Home screen is displayed.
        """
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.login(COMPANY, USERNAME, PASSWORD)
        time.sleep(POST_LOGIN_WAIT)

        assert home_page.is_displayed(), (
            f"Expected Home screen but got {home_page.driver.current_activity}"
        )