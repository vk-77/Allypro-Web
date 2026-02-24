import time
from datetime import datetime
import pytest
from config.settings import COMPANY, USERNAME, PASSWORD, POST_LOGIN_WAIT
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.usefixtures("driver")
class TestHomePage:
    """
    Home page test cases.

    Usage:
        pytest tests/test_home_page.py -s -v
    """

    def test_route_title_and_date(self, driver):
        """
        Verify the Routes title is displayed and the date matches today.
        """
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.login(COMPANY, USERNAME, PASSWORD)
        time.sleep(POST_LOGIN_WAIT)

        # Verify Routes title
        assert home_page.is_displayed(), "Routes title is not displayed"
        title_text = home_page.get_route_title_text()
        print(f"\n  Route Title: {title_text}")
        assert title_text == "Routes", (
            f"Expected title 'Routes' but got '{title_text}'"
        )

        # Verify date is present and matches today
        date_text = home_page.get_date_text()
        today = datetime.now().strftime("%m/%d/%Y")
        print(f"  App Date:    {date_text}")
        print(f"  Today Date:  {today}")
        assert date_text, "Date element is empty"
        assert today in date_text, (
            f"Expected today's date '{today}' in '{date_text}'"
        )

    def test_route_list_displayed(self, driver):
        """
        Verify the route list ScrollView is present on the home screen.
        """
        home_page = HomePage(driver)

        is_displayed = home_page.is_route_list_displayed()
        print(f"\n  Route List Visible: {is_displayed}")
        assert is_displayed, "Route list ScrollView is not displayed"

        # Print all route names
        routes = home_page.get_route_names()
        print(f"  Total Routes: {len(routes)}")
        for i, route in enumerate(routes, 1):
            print(f"  Route {i}: {route}")
        assert len(routes) > 0, "No routes found in the list"
