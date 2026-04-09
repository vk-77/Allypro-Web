"""
Customer Details - transactions tests.

Validates that the Transactions tab loads and displays the billing
history grid on the Customer Details page.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, text_is_visible
from config.web_settings import DEFAULT_WAIT


def _open_customer_details(driver):
    """Navigate to customer details page."""
    page = CustomerPage(driver)
    page.open_customer_details_page()
    return page


@pytest.mark.usefixtures("driver")
class TestTransactions:
    """
    Transactions tests for Customer Details.

    Usage:
        pytest tests/web/customer/test_transactions.py -v
    """

    def test_c56987_transactions_is_working(self, driver):
        """C56987 Transactions is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Transactions tab
        customer_page.open_transactions_tab()
        wait_for_loading_screen(driver)

        # Verify transactions tab content is loaded
        assert text_is_visible(driver, "Transaction", timeout=10) or \
            text_is_visible(driver, "Billing", timeout=10) or \
            text_is_visible(driver, "History", timeout=10), (
            "Transactions tab content should be displayed"
        )

        # Verify the transactions grid/table is present
        transactions_table = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "#parentLiTab_5 ~ .tab-content table, "
            "#billing-history table, "
            ".transactions-grid, "
            "[aria-controls='billing-history'] ~ * table",
        )))
        assert transactions_table is not None, (
            "Transactions grid should be present"
        )
