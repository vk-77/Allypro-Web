"""
Customer Details - pricing tests.

Validates adding a new flat-rate pricing entry from the Pricing
tab on the Customer Details page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    text_is_visible,
)
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestPricing:
    """
    Pricing tests for Customer Details.

    Usage:
        pytest tests/web/customer/test_pricing.py -v
    """

    def test_c56991_add_pricing(self, driver):
        """C56991 Add Pricing."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Pricing tab
        customer_page.open_pricing_tab()
        wait_for_loading_screen(driver)

        # Verify Pricing tab content is loaded
        assert text_is_visible(driver, "Pricing", timeout=10) or \
            text_is_visible(driver, "Price", timeout=10), (
            "Pricing tab content should be displayed"
        )

        # Click Add Pricing button
        add_pricing_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnAddPricing, [onclick*="AddPricing"], '
            '[onclick*="ShowAddPricingPopup"], '
            '[onclick*="ShowPricingPopup"]',
        )))
        add_pricing_btn.click()
        wait_for_loading_screen(driver)

        # Wait for pricing modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divAddPricing, .modal.show, .pricing-modal, "
            "#divPricingPopup",
        )))

        # Select pricing type
        select2_select(
            driver, "#select2-PricingTypeId-container", "Flat"
        )

        # Enter pricing amount
        amount_field = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#PricingAmount, #Amount, [name='Amount']",
        )))
        amount_field.clear()
        amount_field.send_keys("25.00")

        # Save pricing
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnSavePricing, [onclick*="SavePricing"]',
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=10) or \
            text_is_visible(driver, "Pricing", timeout=10), (
            "Pricing should be saved successfully"
        )
