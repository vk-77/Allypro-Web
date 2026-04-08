"""
Billing - Pre-Billing Audits tests.

"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.billing_page import BillingPage
from helpers.web_helper import wait_for_loading_screen, force_click
from config.web_settings import BASE_URL


@pytest.mark.usefixtures("driver")
class TestPreBilling:
    """
    Billing > Pre-Billing Audits tests.

    Usage:
        pytest tests/web/test_06_billing/test_02_pre_billing.py -v
    """

    def _open_pre_billing(self, driver):
        """Navigate to Billing > Pre-Billing Audits."""
        page = BillingPage(driver)
        page.open_pre_billing()
        return page

    # ── C60369 ────────────────────────────────────────────────────

    def test_c60369_view_incomplete_orders(self, driver):
        """C60369 View Incomplete Orders."""
        page = self._open_pre_billing(driver)
        wait_for_loading_screen(driver)

        # Click date range picker (last one) and select Last 7 Days
        date_range_inputs = driver.find_elements(By.CSS_SELECTOR, '[name="dateRange"]')
        assert len(date_range_inputs) > 0, "Date range input should exist"
        driver.execute_script("arguments[0].click();", date_range_inputs[-1])

        last_7 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//*[contains(text(),'Last 7 Days')]"
            ))
        )
        last_7.click()

        # Click load audits
        page.click_element(By.CSS_SELECTOR, '[onclick="GetBillingAuditsPartial();"]')
        wait_for_loading_screen(driver)

        # Click View Incomplete Orders
        page.click_element(By.ID, "btnViewIncompleteOrders")
        wait_for_loading_screen(driver)

        # Should navigate to Operations page
        WebDriverWait(driver, 15).until(EC.url_contains("/Operations?"))
        assert "/Operations?" in driver.current_url, (
            "URL should include /Operations? after viewing incomplete orders"
        )

    # ── Order Details tab ─────────────────────────────────────────

    def test_order_details_tab_is_working(self, driver):
        """Order Details tab is working."""
        page = self._open_pre_billing(driver)

        # Click tab 2
        page.click_element(By.CSS_SELECTOR, "#parentLiTab_2 span")

        # Click 4th button in content area
        page.click_element(By.CSS_SELECTOR, "#content li:nth-child(4) > a.btn")
        wait_for_loading_screen(driver)

        # Click first row action in Audit Summary table
        page.click_element(
            By.CSS_SELECTOR, "#BillingAuditSummaryTable tr:nth-child(1) a.btn"
        )
        wait_for_loading_screen(driver)

        # Verify detail popup modal title is visible
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#BillingAuditSummaryDetailDisplayPopUp h5.modal-title"
        ), "Audit Summary Detail popup title should be visible"

        # Click service code link in detail table
        page.click_element(
            By.CSS_SELECTOR, "#BillingAuditSummaryDetailTable td.serviceCode_td a"
        )
        wait_for_loading_screen(driver)

        # Verify work order label is visible
        assert page.element_is_visible(By.ID, "myWorkOrderLabel"), (
            "Work Order label should be visible"
        )

        # Verify Location Detail text
        location_detail = page.find_visible(
            By.CSS_SELECTOR,
            "#woChildTabContainerOrder_1 div.serviced div.text-center"
        )
        assert location_detail.text == "Location Detail", (
            "Location Detail text should be visible"
        )

        # Click second order tab
        page.click_element(By.CSS_SELECTOR, "#woChildLiTabOrder_2 a.nav-link")
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#woChildTabContainerOrder_2 div.location div.text-center"
        ), "Location tab content should be visible"

        # Close modal dialogs
        page.click_element(By.CSS_SELECTOR, "#divModalHeader button.close")
        page.click_element(
            By.CSS_SELECTOR, "#BillingAuditSummaryDetailDisplayPopUp button.close"
        )
        wait_for_loading_screen(driver)

        # Verify audit detail table span is visible
        assert page.element_is_visible(
            By.CSS_SELECTOR, "#BillingAuditDetailTable span"
        ), "Billing Audit Detail table should still be visible"
