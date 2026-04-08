"""
Customer Details - Bulk Reversal tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from pages.web.base_web_page import BaseWebPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestBulkReversal:
    """
    Verify Bulk Reversal functionality on Customer Details page.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_bulk_reversal.py -v
    """

    def test_c70511_bulk_reversal_option_accessible(self, driver):
        """C70511 Verify Bulk Reversal option is accessible."""
        page = BaseWebPage(driver)

        # Look for Bulk Reversal button or menu option
        assert page.text_is_visible("Bulk Reversal") or page.element_is_visible(
            By.CSS_SELECTOR,
            "[onclick*='BulkReversal'], [data-action='bulk-reversal'], "
            "button[id*='BulkReversal']"
        ), "Bulk Reversal option should be accessible"

    def test_c70512_bulk_reversal_modal_opens(self, driver):
        """C70512 Verify Bulk Reversal modal opens."""
        page = BaseWebPage(driver)

        # Click Bulk Reversal
        page.find_by_text("Bulk Reversal").click()
        wait_for_loading_screen(driver)

        assert page.element_is_visible(By.CSS_SELECTOR, ".modal"), (
            "Bulk Reversal modal should be visible"
        )

        # Close modal
        page.click_element(
            By.CSS_SELECTOR,
            ".modal .close, .modal [data-dismiss='modal'], .modal .btn-close"
        )
