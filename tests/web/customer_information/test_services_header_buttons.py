"""
Customer Details - Services header button tests.

Validates the Add Service and Group Services header buttons for
visibility and click behaviour in the Services section.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestServicesHeaderButtons:
    """
    Verify Add Service and Group Services header buttons.

    Usage:
        pytest tests/web/customer_information/test_services_header_buttons.py -v
    """

    def test_c70520_add_service_button_visible(self, driver):
        """C70520 Verify Add Service button is visible in Services header."""
        page = BasePage(driver)
        assert page.text_is_visible("Add Service") or page.element_is_visible(
            By.CSS_SELECTOR,
            "[onclick*='AddService'], [data-action='add-service'], "
            "button[id*='AddService'], .btn-add-service"
        ), "Add Service button should be visible"

    def test_c70521_group_services_button_visible(self, driver):
        """C70521 Verify Group Services button is visible in Services header."""
        page = BasePage(driver)
        assert page.text_is_visible("Group Services") or page.element_is_visible(
            By.CSS_SELECTOR,
            "[onclick*='GroupService'], [data-action='group-services'], "
            "button[id*='GroupService'], .btn-group-services"
        ), "Group Services button should be visible"
