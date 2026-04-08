"""
Customer Details - Documents and Plans tests.

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
class TestDocumentsAndPlans:
    """
    Documents & Plans tests for Customer Details.

    Usage:
        pytest tests/web/test_01_customer_details/test_12_documents_and_plans.py -v
    """

    def test_c56988_documents_and_plans_is_working(self, driver):
        """C56988 Documents & Plans is working."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Documents tab
        customer_page.open_documents_tab()
        wait_for_loading_screen(driver)

        # Verify documents tab content is loaded
        assert text_is_visible(driver, "Document", timeout=10) or \
            text_is_visible(driver, "Plan", timeout=10), (
            "Documents & Plans tab content should be displayed"
        )

    def test_c56989_create_document_is_displayed(self, driver):
        """C56989 Create Document is displayed."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Documents tab
        customer_page.open_documents_tab()
        wait_for_loading_screen(driver)

        # Click Create Document button
        create_doc_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnCreateDocument, [onclick*="CreateDocument"], '
            '[onclick*="ShowCreateDocumentPopup"], '
            '[onclick*="AddDocument"]',
        )))
        create_doc_btn.click()
        wait_for_loading_screen(driver)

        # Verify Create Document dialog/form is displayed
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divCreateDocument, .modal.show, .document-modal, "
            "#divAddDocument",
        )))

        assert text_is_visible(driver, "Document", timeout=10), (
            "Create Document dialog should be displayed"
        )

    def test_c56990_create_map_plan_is_displayed(self, driver):
        """C56990 Create Map Plan is displayed."""
        wait = WebDriverWait(driver, DEFAULT_WAIT)
        customer_page = _open_customer_details(driver)

        # Open Documents tab
        customer_page.open_documents_tab()
        wait_for_loading_screen(driver)

        # Click Create Map Plan button
        create_plan_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            '#btnCreateMapPlan, [onclick*="CreateMapPlan"], '
            '[onclick*="ShowCreateMapPlanPopup"], '
            '[onclick*="AddMapPlan"]',
        )))
        create_plan_btn.click()
        wait_for_loading_screen(driver)

        # Verify Create Map Plan dialog/form is displayed
        wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#divCreateMapPlan, .modal.show, .map-plan-modal, "
            "#divAddMapPlan",
        )))

        assert text_is_visible(driver, "Map", timeout=10) or \
            text_is_visible(driver, "Plan", timeout=10), (
            "Create Map Plan dialog should be displayed"
        )
