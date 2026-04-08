"""
Receivables - Auto Apply tests.

"""
import re
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.web.receivables_page import ReceivablesPage
from helpers.web_helper import (
    click_submenu,
    wait_for_loading_screen,
    select2_select_option,
    scroll_to_element,
    force_click,
)


@pytest.mark.usefixtures("driver")
class TestAutoApply:
    """
    Verify Auto Apply billing cycle, load, clear, column validation, and process.

    Usage:
        pytest tests/web/test_08_receivables/test_02_auto_apply.py -v
    """

    def _navigate_to_auto_apply(self, driver):
        """Navigate to Receivables > Auto Apply."""
        page = ReceivablesPage(driver)
        page.open_auto_apply()
        return page

    def _select_billing_cycle_28day(self, driver):
        """Select '28 Day' billing cycle via Select2 dropdown."""
        select2_select_option(
            driver,
            "#select2-ddlBillingCycle-container",
            "28 Day",
            "28 Day - 28 day",
        )
        # Verify selection
        container = driver.find_element(By.ID, "select2-ddlBillingCycle-container")
        assert "Day" in container.text, "Billing cycle should contain 'Day'"

    def _click_load_payment_credit(self, driver):
        """Click Load button for payment credits."""
        wait = WebDriverWait(driver, 15)
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a.btn.btn-primary[onclick="LoadPaymentCredit()"]')
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

    def test_c69980_billing_cycle_dropdown_is_working(self, driver):
        """C69980 Billing Cycle dropdown is working."""
        self._navigate_to_auto_apply(driver)

        wait = WebDriverWait(driver, 10)

        # Verify dropdown exists and is visible
        dropdown = wait.until(EC.visibility_of_element_located(
            (By.ID, "ddlBillingCycle")
        ))

        # Verify it has at least 1 option
        options = dropdown.find_elements(By.TAG_NAME, "option")
        assert len(options) >= 1, "Billing cycle dropdown should have at least 1 option"

        # Select first available option (skip default empty)
        if len(options) > 1:
            first_value = options[1].get_attribute("value")
            if first_value:
                Select(dropdown).select_by_value(first_value)
                assert dropdown.get_attribute("value") == first_value, (
                    "Selected value should match"
                )

    def test_c69981_load_billing_cycle_without_selection(self, driver):
        """C69981 Load Billing cycle without selection a range."""
        self._navigate_to_auto_apply(driver)

        wait = WebDriverWait(driver, 10)

        # Verify dropdown has no selection
        dropdown = driver.find_element(By.ID, "ddlBillingCycle")
        assert dropdown.get_attribute("value") == "", (
            "Billing cycle should have no selection initially"
        )

        # Click Load without selecting a billing cycle
        load_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[onclick="LoadPaymentCredit()"]')
        ))
        load_btn.click()
        wait_for_loading_screen(driver)

        # Validate no record message
        no_record = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".norecord1")
        ))
        assert "No record exist" in no_record.text, (
            "Should display 'No record exist' message"
        )

    def test_c69982_clear_button_is_working(self, driver):
        """C69982 Clear button is working."""
        self._navigate_to_auto_apply(driver)

        # Select billing cycle via Select2
        self._select_billing_cycle_28day(driver)

        # Click Load
        self._click_load_payment_credit(driver)

        # Click Clear
        wait = WebDriverWait(driver, 10)
        clear_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[onclick="clearFilter()"]')
        ))
        clear_btn.click()

        # Validate dropdown is reset
        dropdown = driver.find_element(By.ID, "ddlBillingCycle")
        assert dropdown.get_attribute("value") == "", (
            "Billing cycle should be cleared"
        )

    def test_c69983_validate_columns_format_and_tooltip(self, driver):
        """C69983 Validate columns format and tooltip."""
        self._navigate_to_auto_apply(driver)

        # Select billing cycle
        self._select_billing_cycle_28day(driver)

        # Click Load
        self._click_load_payment_credit(driver)

        wait = WebDriverWait(driver, 10)

        # Validate table is visible
        wait.until(EC.visibility_of_element_located(
            (By.ID, "paymentCreditTable")
        ))
        assert driver.find_element(
            By.CSS_SELECTOR, "#paymentCreditTable thead"
        ), "Table header should exist"
        assert driver.find_element(
            By.ID, "DispatchBodyRowContainer"
        ), "Body row container should exist"

        # Validate tooltip on watch icon
        watch_icons = driver.find_elements(
            By.CSS_SELECTOR,
            'a.watch-icon[data-original-title*="Partially Applied"], '
            'a.watch-icon[title*="Partially Applied"]'
        )
        if watch_icons:
            icon = watch_icons[0]
            scroll_to_element(driver, icon)
            ActionChains(driver).move_to_element(icon).perform()

            # Wait for tooltip to appear
            tooltip = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".tooltip")
            ))
            tooltip_text = tooltip.text
            assert "Partially Applied" in tooltip_text, (
                "Tooltip should contain 'Partially Applied'"
            )
            assert "Not Applied" in tooltip_text, (
                "Tooltip should contain 'Not Applied'"
            )

        # Validate first row has 8 columns
        first_row = driver.find_element(
            By.CSS_SELECTOR, "#DispatchBodyRowContainer tr"
        )
        cells = first_row.find_elements(By.TAG_NAME, "td")
        assert len(cells) == 8, f"First row should have 8 columns, got {len(cells)}"

        # Validate Amount (column 7) format
        amount_text = cells[6].text.strip()
        assert re.match(r'^-?\d+(\.\d{2})?$', amount_text), (
            f"Amount '{amount_text}' should be in currency format"
        )

        # Validate Balance (column 8) format
        balance_text = cells[7].text.strip()
        assert re.match(r'^-?\d+(\.\d{2})?$', balance_text), (
            f"Balance '{balance_text}' should be in currency format"
        )

        # Validate Date (column 4) format MM/DD/YYYY
        date_text = cells[3].text.strip()
        assert re.match(r'^\d{2}/\d{2}/\d{4}$', date_text), (
            f"Date '{date_text}' should be in MM/DD/YYYY format"
        )

    def test_c69984_auto_apply_payment_credit_process(self, driver):
        """C69984 Auto Apply Payment Credit process."""
        self._navigate_to_auto_apply(driver)

        wait = WebDriverWait(driver, 15)

        # Select billing cycle
        self._select_billing_cycle_28day(driver)

        # Click Load
        self._click_load_payment_credit(driver)

        # Click Auto Apply button to open confirmation modal
        auto_apply_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "btnAutoApply")
        ))
        scroll_to_element(driver, auto_apply_btn)
        auto_apply_btn.click()
        wait_for_loading_screen(driver)

        # Validate confirmation modal is visible
        wait.until(EC.visibility_of_element_located(
            (By.ID, "myReverseModal-container")
        ))

        # Validate confirmation text
        modal_title = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "#myReverseModal-container h3.modal-title.transaction_title"
        )))
        modal_text = modal_title.text
        assert "automatically apply any unapplied payments" in modal_text, (
            "Modal should describe auto apply action"
        )
        assert "Do you want to proceed" in modal_text, (
            "Modal should ask for confirmation"
        )

        # Click YES to start the auto-apply process
        confirm_btn = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "#myReverseModal-container #btnAutoApplyPaymentCredit"
        )))
        scroll_to_element(driver, confirm_btn)
        driver.execute_script("arguments[0].click();", confirm_btn)

        wait_for_loading_screen(driver)

        # Check for In-progress button (may be short-lived)
        in_progress_btns = driver.find_elements(
            By.ID, "btnAutoApplyPaymentCreditInprogress"
        )
        if in_progress_btns:
            assert "In-progress" in in_progress_btns[0].text, (
                "In-progress button should display 'In-progress'"
            )
