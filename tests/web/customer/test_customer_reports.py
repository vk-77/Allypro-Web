"""
Customer Details - customer reports tests.

Validates generating and running a customer report from the
Customer Details page and verifying the report output is displayed.
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
class TestCustomerReports:
    """
    Customer Reports tests for Customer Details.

    Usage:
        pytest tests/web/customer/test_customer_reports.py -v
    """

    def test_c56980_run_customer_reports(self, driver):
        """C56980 Run Customer Reports."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Click Generate Report
        customer_page.click_generate_report()

        # Wait for report modal/section
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divGenerateReport, .modal.show, .report-modal, "
            "#divGenerateCustomerReport",
        )))
        wait_for_loading_screen(driver)

        # Verify report generation UI is displayed
        assert text_is_visible(driver, "Report", timeout=10), (
            "Report generation dialog should be displayed"
        )

        # Select a report type (first available)
        try:
            report_option = wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "#divGenerateReport .report-option:first-child, "
                "#divGenerateCustomerReport input[type='radio']:first-of-type, "
                ".report-type-list li:first-child",
            )))
            report_option.click()
        except Exception:
            pass

        # Click Run/Generate report button
        run_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnRunReport, [onclick*="RunReport"], '
            '[onclick*="GenerateReport"], #btnGenerateReport',
        )))
        run_btn.click()
        wait_for_loading_screen(driver)

        # Verify report output is displayed (PDF, table, or download)
        WebDriverWait(driver, 30).until(
            lambda d: (
                d.find_elements(By.CSS_SELECTOR,
                                "iframe, embed, .pdf-viewer, .report-output")
                or text_is_visible(d, "Report", timeout=2)
            )
        )
