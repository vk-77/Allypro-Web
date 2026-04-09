"""
Customer Details - Service Location widget tests.

Validates the Service Location widget visibility, location ID, address
fields, and dropdown menu options on the Information tab.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BasePage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestServiceLocationWidget:
    """
    Verify Service Location widget fields on the Information tab.

    Usage:
        pytest tests/web/customer_information/test_service_location_widget.py -v
    """

    def test_c70477_service_location_widget_visible(self, driver):
        """C70477 Verify Service Location widget is visible."""
        page = BasePage(driver)
        assert page.text_is_visible("Service Location") or page.element_is_visible(
            By.CSS_SELECTOR, ".service-location, .service-location-widget"
        ), "Service Location widget should be visible"

    def test_c70478_service_location_displays_id(self, driver):
        """C70478 Verify Service Location displays location ID."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            "#InformationTabInfo_ServiceLocationIDDash, "
            ".service-location [id*='LocationID']"
        ), "Service Location ID should be displayed"

    def test_c70479_service_location_displays_address(self, driver):
        """C70479 Verify Service Location displays address."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .address, "
            ".service-location-widget [id*='Address']"
        ), "Service Location address should be displayed"

    def test_c70480_service_location_displays_city_state_zip(self, driver):
        """C70480 Verify Service Location displays city, state, zip."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .cityStateZip, "
            ".service-location-widget [id*='CityStateZip']"
        ), "Service Location city/state/zip should be displayed"

    def test_c70481_service_location_displays_phone(self, driver):
        """C70481 Verify Service Location displays phone number."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .phone, "
            ".service-location-widget [id*='Phone']"
        ), "Service Location phone should be displayed"

    def test_c70482_service_location_displays_contact(self, driver):
        """C70482 Verify Service Location displays contact name."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .contact, "
            ".service-location-widget [id*='Contact']"
        ), "Service Location contact should be displayed"

    def test_c70483_service_location_displays_email(self, driver):
        """C70483 Verify Service Location displays email."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .email, "
            ".service-location-widget [id*='Email']"
        ), "Service Location email should be displayed"

    def test_c70484_service_location_displays_status(self, driver):
        """C70484 Verify Service Location displays status."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .status, "
            ".service-location-widget [id*='Status']"
        ), "Service Location status should be displayed"

    def test_c70485_service_location_has_dropdown_menu(self, driver):
        """C70485 Verify Service Location widget has a dropdown menu."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .dropdown-toggle, "
            ".service-location-widget .dropdown-toggle"
        ), "Service Location dropdown toggle should be visible"

    def test_c70486_service_location_displays_zone(self, driver):
        """C70486 Verify Service Location displays zone information."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .zone, "
            ".service-location-widget [id*='Zone']"
        ) or page.text_is_visible("Zone"), "Zone info should be displayed"

    def test_c70487_service_location_displays_type(self, driver):
        """C70487 Verify Service Location displays type."""
        page = BasePage(driver)
        assert page.element_is_visible(
            By.CSS_SELECTOR,
            ".service-location .type, "
            ".service-location-widget [id*='Type']"
        ) or page.text_is_visible("Type"), "Service Location type should be displayed"
