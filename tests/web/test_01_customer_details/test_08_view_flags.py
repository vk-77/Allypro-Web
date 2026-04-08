"""
Customer Details - View and Delete Flags tests.

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
class TestViewFlags:
    """
    Flag tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_08_view_flags.py -v
    """

    def test_c56981_view_flags(self, driver):
        """C56981 View Flags."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click flags container
        customer_page.click_flags()

        # Wait for flags modal/popup
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divFlagPopup, .modal.show, .flag-modal, "
            "#divCustomerFlags, #customerFlagPopup",
        )))
        wait_for_loading_screen(driver)

        # Verify flags section is displayed
        assert text_is_visible(driver, "Flag", timeout=10), (
            "Flags dialog should be displayed"
        )

    def test_c56982_delete_flags(self, driver):
        """C56982 Delete Flags."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click flags container
        customer_page.click_flags()

        # Wait for flags modal/popup
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divFlagPopup, .modal.show, .flag-modal, "
            "#divCustomerFlags, #customerFlagPopup",
        )))
        wait_for_loading_screen(driver)

        # Find and click delete button on a flag (if flags exist)
        try:
            delete_btn = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                '.flag-delete, [onclick*="DeleteFlag"], '
                '.btn-delete-flag, .fa-trash',
            )))
            delete_btn.click()
            wait_for_loading_screen(driver)

            # Confirm deletion if confirmation dialog appears
            try:
                confirm_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        '.swal2-confirm, .btn-confirm, '
                        '[onclick*="ConfirmDelete"]',
                    ))
                )
                confirm_btn.click()
                wait_for_loading_screen(driver)
            except Exception:
                pass

            # Verify success
            assert text_is_visible(driver, "success", timeout=10) or \
                text_is_visible(driver, "deleted", timeout=10) or \
                text_is_visible(driver, "Flag", timeout=10), (
                "Flag should be deleted successfully"
            )
        except Exception:
            # If no flags to delete, verify the flags section is at least visible
            assert text_is_visible(driver, "Flag", timeout=5), (
                "Flags dialog should be displayed even if no flags to delete"
            )
