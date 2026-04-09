"""
Customer Details - Service Activity work order Audit tab tests.

Validates that the Audit tab link is visible and opens the audit log
pane within the work order modal.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen
from config.web_settings import DEFAULT_WAIT


@pytest.mark.usefixtures("driver")
class TestModalAudit:
    """
    Service Activity tab - work order Audit tab.

    """

    def test_c339632_audit_tab_link_visible_and_opens(self, driver):
        """C339632 Audit tab: Verify link is visible and opens the Audit tab."""
        page = CustomerPage(driver)
        page.open_work_order_modal_tab(page.WO_TAB_AUDIT, page.WO_PANE_AUDIT)
        # Verify the pane is visible and active
        pane = page.find_visible(*page.WO_PANE_AUDIT, timeout=15)
        assert "active" in pane.get_attribute("class")
