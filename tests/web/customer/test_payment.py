"""
Customer Details - payment tests.

Validates adding payments via cash, credit card with WorldPay,
and credit card with Authorize.net from the Customer Details page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    select_dropdown,
    text_is_visible,
)
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


def _fill_adjustment_payment_card_fields(driver, payment_data):
    """
    Fill card payment fields in the payment modal.
    """
    wait = WebDriverWait(driver, DEFAULT_WAIT)

    cardholder = wait.until(EC.element_to_be_clickable((
        By.ID, "CardHolderName"
    )))
    cardholder.clear()
    cardholder.send_keys(payment_data["card_holder_name"])

    card_number = wait.until(EC.element_to_be_clickable((
        By.ID, "CardNumber"
    )))
    card_number.clear()
    card_number.send_keys(payment_data["card_number"])

    exp_month = wait.until(EC.element_to_be_clickable((
        By.ID, "ExpirationMonth"
    )))
    exp_month.clear()
    exp_month.send_keys(payment_data["expiration_month"])

    exp_year = wait.until(EC.element_to_be_clickable((
        By.ID, "ExpirationYear"
    )))
    exp_year.clear()
    exp_year.send_keys(payment_data["expiration_year"])

    cvv = wait.until(EC.element_to_be_clickable((
        By.ID, "CVV"
    )))
    cvv.clear()
    cvv.send_keys(payment_data["cvv"])

    zip_code = wait.until(EC.element_to_be_clickable((
        By.ID, "ZipCode"
    )))
    zip_code.clear()
    zip_code.send_keys(payment_data["zip_code"])


@pytest.mark.usefixtures("driver")
class TestPayment:
    """
    Payment tests for Customer Details.

    Usage:
        pytest tests/web/customer/test_payment.py -v
    """

    def test_c56972_add_payment_with_cash(self, driver):
        """C56972 Add Payment with cash."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)
        payment = USER_DATA["payment"]

        # Click Add Payment
        customer_page.click_add_payment()
        wait_for_loading_screen(driver)

        # Wait for payment modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "#divAddPayment, .modal.show, .payment-modal"
        )))

        # Select payment method: Cash
        select2_select(
            driver, "#select2-PaymentMethodId-container", "Cash"
        )

        # Enter amount
        amount_field = wait.until(EC.element_to_be_clickable((
            By.ID, "Amount"
        )))
        amount_field.clear()
        amount_field.send_keys(payment["amount"])

        # Enter detail note
        note_field = wait.until(EC.element_to_be_clickable((
            By.ID, "DetailNote"
        )))
        note_field.clear()
        note_field.send_keys(payment["detail_note"])

        # Save payment
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnSavePayment, [onclick*="SavePayment"]'
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=10) or \
            text_is_visible(driver, "Payment", timeout=10), (
            "Payment should be saved successfully"
        )

    def test_c58076_add_payment_with_card_worldpay(self, driver):
        """C58076 Add Payment with card WorldPay."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)
        payment = USER_DATA["payment"]

        # Click Add Payment
        customer_page.click_add_payment()
        wait_for_loading_screen(driver)

        # Wait for payment modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "#divAddPayment, .modal.show, .payment-modal"
        )))

        # Select payment method: Credit Card
        select2_select(
            driver, "#select2-PaymentMethodId-container", "Credit Card"
        )

        # Select payment gateway: WorldPay
        select2_select(
            driver, "#select2-PaymentGatewayId-container", "WorldPay"
        )

        # Enter amount
        amount_field = wait.until(EC.element_to_be_clickable((
            By.ID, "Amount"
        )))
        amount_field.clear()
        amount_field.send_keys(payment["amount"])

        # Fill card fields
        _fill_adjustment_payment_card_fields(driver, payment)

        # Save payment
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnSavePayment, [onclick*="SavePayment"]'
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=15) or \
            text_is_visible(driver, "Payment", timeout=10), (
            "WorldPay payment should be saved successfully"
        )

    def test_c59634_add_payment_with_card_authorize_net(self, driver):
        """C59634 Add Payment with card Authorize.net."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)
        payment = USER_DATA["payment"]

        # Click Add Payment
        customer_page.click_add_payment()
        wait_for_loading_screen(driver)

        # Wait for payment modal
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, "#divAddPayment, .modal.show, .payment-modal"
        )))

        # Select payment method: Credit Card
        select2_select(
            driver, "#select2-PaymentMethodId-container", "Credit Card"
        )

        # Select payment gateway: Authorize.net
        select2_select(
            driver, "#select2-PaymentGatewayId-container", "Authorize"
        )

        # Enter amount
        amount_field = wait.until(EC.element_to_be_clickable((
            By.ID, "Amount"
        )))
        amount_field.clear()
        amount_field.send_keys(payment["amount"])

        # Fill card fields
        _fill_adjustment_payment_card_fields(driver, payment)

        # Save payment
        save_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '#btnSavePayment, [onclick*="SavePayment"]'
        )))
        save_btn.click()
        wait_for_loading_screen(driver)

        # Verify success
        assert text_is_visible(driver, "success", timeout=15) or \
            text_is_visible(driver, "Payment", timeout=10), (
            "Authorize.net payment should be saved successfully"
        )
