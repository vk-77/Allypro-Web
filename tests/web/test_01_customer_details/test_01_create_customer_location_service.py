"""
Customer Details - Create Customer, Location, and Service.

"""
import pytest
from faker import Faker

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    navigate_to_menu,
    select2_select,
    select2_select_option,
    select_dropdown,
    force_click,
    text_is_visible,
)
from config.web_settings import DEFAULT_WAIT

fake = Faker()


@pytest.mark.usefixtures("driver")
class TestCreateCustomerLocationService:
    """
    C341598 - Create Customer Location and Service.

    Full wizard flow: customer > contact > settings > custom fields >
    location > service > routing > workflow.

    Usage:
        pytest tests/web/test_01_customer_details/test_01_create_customer_location_service.py -v
    """

    def test_c341598_create_customer_location_and_service(self, driver):
        """C341598 Create Customer Location and Service."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_name = fake.last_name() + fake.first_name()[:4]
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.numerify("##########")
        address_line = fake.street_address()

        # ── Step 1: Navigate to Customers menu and open Create Customer ──
        navigate_to_menu(driver, "Customers")
        wait_for_loading_screen(driver)

        create_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[onclick="CreateNewCustomer()"]'
        )))
        create_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 2: Customer Information ─────────────────────────────────
        # Customer name
        name_field = wait.until(EC.element_to_be_clickable((
            By.ID, "CustomerName"
        )))
        name_field.clear()
        name_field.send_keys(customer_name)

        # Customer type dropdown
        select2_select(driver, "#select2-CustomerTypeId-container", "Commercial")

        # Status
        select2_select(driver, "#select2-StatusId-container", "Active")

        # Click Next to go to Contact step
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnCustomerNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 3: Contact Information ──────────────────────────────────
        first_name_field = wait.until(EC.element_to_be_clickable((
            By.ID, "FirstName"
        )))
        first_name_field.clear()
        first_name_field.send_keys(first_name)

        last_name_field = wait.until(EC.element_to_be_clickable((
            By.ID, "LastName"
        )))
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        email_field = wait.until(EC.element_to_be_clickable((
            By.ID, "Email"
        )))
        email_field.clear()
        email_field.send_keys(email)

        phone_field = wait.until(EC.element_to_be_clickable((
            By.ID, "Phone"
        )))
        phone_field.clear()
        phone_field.send_keys(phone)

        # Click Next to go to Settings step
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnContactNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 4: Settings ─────────────────────────────────────────────
        # Billing cycle
        select2_select(
            driver, "#select2-BillingCycleId-container", "Monthly"
        )

        # Payment terms
        select2_select(
            driver, "#select2-PaymentTermId-container", "Net 30"
        )

        # Click Next to Custom Fields
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnSettingsNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 5: Custom Fields ────────────────────────────────────────
        # Click Next (custom fields may be optional)
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnCustomFieldNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 6: Location ─────────────────────────────────────────────
        address_field = wait.until(EC.element_to_be_clickable((
            By.ID, "ServiceAddress"
        )))
        address_field.clear()
        address_field.send_keys(address_line)

        city_field = wait.until(EC.element_to_be_clickable((
            By.ID, "ServiceCity"
        )))
        city_field.clear()
        city_field.send_keys("New York")

        state_field = wait.until(EC.element_to_be_clickable((
            By.ID, "ServiceState"
        )))
        state_field.clear()
        state_field.send_keys("NY")

        zip_field = wait.until(EC.element_to_be_clickable((
            By.ID, "ServiceZip"
        )))
        zip_field.clear()
        zip_field.send_keys("10001")

        # Click Next to go to Service step
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnLocationNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 7: Service ──────────────────────────────────────────────
        # Service type
        select2_select(
            driver, "#select2-ServiceTypeId-container", "Waste"
        )

        # Frequency
        select2_select(
            driver, "#select2-FrequencyId-container", "Weekly"
        )

        # Click Next to Routing
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnServiceNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 8: Routing ──────────────────────────────────────────────
        # Click Next to Workflow (routing may be optional)
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnRoutingNext, [onclick*="nextStep"], .btn-next'
        )))
        next_btn.click()
        wait_for_loading_screen(driver)

        # ── Step 9: Workflow / Save ──────────────────────────────────────
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnSaveCustomer, [onclick*="SaveCustomer"], .btn-save, .btn-finish',
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # ── Verify customer was created ──────────────────────────────────
        WebDriverWait(driver, 15).until(
            lambda d: "/CustomerDetails" in d.current_url
        )
        assert "/CustomerDetails" in driver.current_url, (
            "Should navigate to Customer Details after creation"
        )

        # Verify customer name appears on the details page
        assert text_is_visible(driver, customer_name, timeout=10), (
            f"Customer name '{customer_name}' should appear on the details page"
        )
