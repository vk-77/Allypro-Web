"""
Home - User Preferences tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestUserPreferences:
    """
    Verify user preferences modal and dropdown fields.

    Usage:
        pytest tests/web/test_10_home/test_02_user_preferences.py -v
    """

    def test_c70186_home_screen_displays_user_preferences(self, driver):
        """C70186 Verify home screen displays user preferences with dropdowns."""
        home_page = HomeWebPage(driver)

        # Open user sidebar
        home_page.open_user_info()

        # Click User Preferences link
        user_pref_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(),'User Preferences')]")
            )
        )
        user_pref_link.click()
        wait_for_loading_screen(driver)

        # Verify USER PREFERENCE modal title is visible
        modal_title = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'USER PREFERENCE')]")
            )
        )
        assert modal_title.is_displayed(), (
            "USER PREFERENCE title should be visible in the modal"
        )

        # Verify Left dropdown is visible
        ddl_left = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ddlHomeScreenLeft"))
        )
        assert ddl_left.is_displayed(), (
            "Left home screen dropdown should be visible"
        )

        # Verify Middle dropdown is visible
        ddl_middle = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ddlHomeScreenMiddle"))
        )
        assert ddl_middle.is_displayed(), (
            "Middle home screen dropdown should be visible"
        )

        # Verify Right dropdown is visible
        ddl_right = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ddlHomeScreenRight"))
        )
        assert ddl_right.is_displayed(), (
            "Right home screen dropdown should be visible"
        )
