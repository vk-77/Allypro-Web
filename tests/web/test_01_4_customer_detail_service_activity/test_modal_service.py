"""
Customer Details - Service Activity tab - calendar order modal (work order modal shell).

"""
import re
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, force_click
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT


ORDER_MODAL_TAB_LABELS = [
    "Information", "Access", "Billing / Disposal / Labor", "Equipment",
    "Attachments", "Status History", "Events", "Audit",
]


def _open_work_order(driver):
    """Open today's work order from the calendar."""
    page = CustomerPage(driver)
    page.open_work_order_from_calendar_today()
    return page


@pytest.mark.usefixtures("driver")
class TestModalService:
    """
    Service Activity tab - calendar order modal (svcHisCalendar).

    """

    def test_c339676_calendar_event_opens_order_modal_validates_header(self, driver):
        """C339676 clicking calendar event opens order modal and validates header fields."""
        page = _open_work_order(driver)
        modal = page.find_visible(*page.WO_MODAL_WRAPPER, timeout=20)

        # Header
        header = page.find_visible(*page.WO_MODAL_HEADER)
        assert header.is_displayed()

        # Title: Order #XXX | Service:... | Workflow:
        title = page.find_visible(*page.WO_MODAL_TITLE)
        title_text = re.sub(r'\s+', ' ', title.text).strip()
        assert re.search(r'Order #\d+\s*\|\s*Service:.+\|\s*Workflow:', title_text, re.IGNORECASE)

        # Body
        body = page.find_visible(*page.WO_MODAL_BODY)
        assert body.is_displayed()

        # Top info
        top_info = page.find_visible(*page.WO_MODAL_TOP_INFO)
        assert top_info.is_displayed()

        # Location, Workflow, Service Date
        for label in ["Location:", "Workflow:", "Service Date:"]:
            info_el = top_info.find_element(
                By.XPATH,
                f'.//*[contains(@class,"clsordertop-info-inner") and contains(text(),"{label}")]'
            )
            assert info_el.is_displayed()
            span = info_el.find_element(By.TAG_NAME, "span")
            assert len(span.text.strip()) >= 1

        # Service Date format MM/DD/YYYY
        date_el = top_info.find_element(
            By.XPATH,
            './/*[contains(@class,"clsordertop-info-inner") and contains(text(),"Service Date:")]'
        )
        date_span = date_el.find_element(By.TAG_NAME, "span")
        assert re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_span.text.strip())

        # Tabs
        tabs_list = page.find_visible(*page.WO_MODAL_TABS_LIST)
        assert tabs_list.is_displayed()
        for label in ORDER_MODAL_TAB_LABELS:
            tab_link = tabs_list.find_element(
                By.XPATH, f'.//a[contains(@class,"nav-link") and contains(text(),"{label}")]'
            )
            assert tab_link.is_displayed()

    def test_c339677_send_sms_validate(self, driver):
        """C339677 Send SMS: validate functionality."""
        page = _open_work_order(driver)
        # Open SMS modal
        sms_btn = page.find_visible(*page.WO_SMS_OPEN_BTN, timeout=15)
        sms_btn.click()
        sms_modal = page.find_visible(*page.MODAL_ORDER_DETAIL_SMS, timeout=15)
        title = sms_modal.find_element(By.CSS_SELECTOR, ".modal-title")
        assert re.search(r"send sms", title.text, re.IGNORECASE)

        # Select template
        template_label = USER_DATA.get("payment", {}).get("card_holder_name", "").strip()
        assert len(template_label) >= 1
        template_select = page.find_visible(*page.DDL_ORDER_SMS_TEMPLATE, timeout=10)
        Select(template_select).select_by_visible_text(template_label)
        assert template_select.get_attribute("value")

        # Contact Suggestions
        contact_icon = sms_modal.find_element(By.ID, "txtShowPoNumberCopy")
        contact_icon.click()
        suggestions_modal = page.find_visible(*page.MODAL_CONTACT_SUGGESTIONS, timeout=15)
        header = suggestions_modal.find_element(By.ID, "spnRegionHeader")
        assert "Contact" in header.text
        # Customer tab
        cust_tab = suggestions_modal.find_element(
            By.CSS_SELECTOR, "#parentLiTabHistory_2 a"
        )
        cust_tab.click()
        WebDriverWait(driver, 5).until(
            lambda d: "active" in d.find_element(
                By.CSS_SELECTOR, "#modalContactSuggestions #parentLiTabHistory_2"
            ).get_attribute("class")
        )
        # Other Locations tab
        other_tab = suggestions_modal.find_element(
            By.CSS_SELECTOR, "#parentLiTabHistory_3 a"
        )
        other_tab.click()
        WebDriverWait(driver, 5).until(
            lambda d: "active" in d.find_element(
                By.CSS_SELECTOR, "#modalContactSuggestions #parentLiTabHistory_3"
            ).get_attribute("class")
        )
        # Close suggestions
        close_btn = suggestions_modal.find_element(By.CSS_SELECTOR, "button.close")
        close_btn.click()
        assert page.element_not_visible(*page.MODAL_CONTACT_SUGGESTIONS, timeout=10)

        # Enter contact and send
        raw_mobile = USER_DATA.get("mobile", "").strip()
        contact = raw_mobile if raw_mobile.startswith("+") else f"+1{raw_mobile}"
        contact_input = page.find_visible(*page.TXT_ORDER_SMS_CONTACT, timeout=10)
        contact_input.clear()
        contact_input.send_keys(contact)
        send_btn = page.find_visible(*page.BTN_ORDER_SMS_SEND)
        send_btn.click()
        wait_for_loading_screen(driver)

        # Verify success banner
        WebDriverWait(driver, 20).until(
            lambda d: any(
                re.search(r"success|sent|SMS|message", el.text, re.IGNORECASE)
                for el in d.find_elements(
                    By.CSS_SELECTOR, "#displayMsg, #msgBillAlert, #divSucessContent"
                )
                if el.text.strip()
            )
        )

    def test_c339681_send_email_validate(self, driver):
        """C339681 Send Email: validate functionality."""
        page = _open_work_order(driver)
        # Open Email modal
        email_btn = page.find_visible(*page.WO_EMAIL_OPEN_BTN, timeout=15)
        email_btn.click()
        email_modal = page.find_visible(*page.MODAL_SEND_OPS_EMAIL, timeout=15)
        header = email_modal.find_element(By.ID, "hPrintOrderHeader")
        assert re.search(r"email order", header.text, re.IGNORECASE)

        # Enter email
        email_input = email_modal.find_element(*page.TXT_OPS_EMAIL_ADDRESS)
        email_input.clear()
        email_input.send_keys(USER_DATA["email"])

        # Contact Suggestions
        contact_icon = email_modal.find_element(By.ID, "txtShowPoNumberCopy")
        contact_icon.click()
        suggestions_modal = page.find_visible(*page.MODAL_CONTACT_SUGGESTIONS, timeout=15)
        header = suggestions_modal.find_element(By.ID, "spnRegionHeader")
        assert "Contact" in header.text
        # Customer tab
        cust_tab = suggestions_modal.find_element(By.CSS_SELECTOR, "#parentLiTabHistory_2 a")
        cust_tab.click()
        # Other Locations tab
        other_tab = suggestions_modal.find_element(By.CSS_SELECTOR, "#parentLiTabHistory_3 a")
        other_tab.click()
        # Close
        close_btn = suggestions_modal.find_element(By.CSS_SELECTOR, "button.close")
        close_btn.click()
        assert page.element_not_visible(*page.MODAL_CONTACT_SUGGESTIONS, timeout=10)

        # Template
        template_select = email_modal.find_element(*page.DDL_PRINT_ORDER_TEMPLATE)
        sel = Select(template_select)
        assert len(sel.options) > 1
        sel.select_by_index(1)
        assert template_select.get_attribute("value")

        # Include Selected Attachments (should be disabled)
        att_chk = email_modal.find_element(*page.CHK_INCLUDE_SELECTED_ATTACHMENTS)
        assert not att_chk.is_enabled()

        # Include Order PDF
        pdf_chk = email_modal.find_element(*page.CHK_INCLUDE_ORDER_PDF)
        assert not pdf_chk.is_selected()
        assert pdf_chk.is_enabled()
        force_click(driver, *page.CHK_INCLUDE_ORDER_PDF)
        pdf_chk = email_modal.find_element(*page.CHK_INCLUDE_ORDER_PDF)
        assert pdf_chk.is_selected()

        # Send
        send_btn = email_modal.find_element(*page.BTN_EMAIL_ORDER)
        send_btn.click()
        wait_for_loading_screen(driver)

        # Success banner
        WebDriverWait(driver, 20).until(
            lambda d: any(
                re.search(r"success|sent|email|message", el.text, re.IGNORECASE)
                for el in d.find_elements(
                    By.CSS_SELECTOR, "#displayMsg, #msgBillAlert, #divSucessContent"
                )
                if el.text.strip()
            )
        )

        # Cancel closes modal
        # Re-open if closed
        modals = driver.find_elements(*page.MODAL_SEND_OPS_EMAIL)
        if not any(m.is_displayed() for m in modals):
            email_btn = page.find_visible(*page.WO_EMAIL_OPEN_BTN, timeout=15)
            email_btn.click()
        page.find_visible(*page.MODAL_SEND_OPS_EMAIL, timeout=15)
        cancel_btn = driver.find_element(
            By.CSS_SELECTOR, '#sendOpsAlertEmailPopUp input[type="button"][value="Cancel"]'
        )
        cancel_btn.click()
        assert page.element_not_visible(*page.MODAL_SEND_OPS_EMAIL, timeout=10)

    def test_c339678_print_order_modal(self, driver):
        """C339678 Print Order: open modal, AlphaV3 template, Print opens PDF, Cancel closes."""
        page = _open_work_order(driver)
        print_btn = page.find_visible(*page.WO_PRINT_OPEN_BTN, timeout=15)
        print_btn.click()
        email_modal = page.find_visible(*page.MODAL_SEND_OPS_EMAIL, timeout=15)
        header = email_modal.find_element(By.ID, "hPrintOrderHeader")
        assert re.search(r"print order", header.text, re.IGNORECASE)

        # Template selection
        template_select = email_modal.find_element(*page.DDL_PRINT_ORDER_TEMPLATE)
        sel = Select(template_select)
        assert len(sel.options) > 3
        sel.select_by_visible_text("AlphaV3")
        assert template_select.get_attribute("value")

        # Print button
        print_order_btn = email_modal.find_element(*page.BTN_PRINT_ORDER)
        # Intercept window.open before clicking
        driver.execute_script("window.__printUrl = null; window.open = function(url) { window.__printUrl = url; };")
        print_order_btn.click()
        wait_for_loading_screen(driver)
        # Verify window.open was called with PDF URL
        print_url = driver.execute_script("return window.__printUrl;")
        assert print_url is not None and len(print_url) >= 1
        assert re.search(r"pdf|Downloads|Resources", print_url, re.IGNORECASE)

        # Cancel closes modal
        cancel_btn = driver.find_element(
            By.CSS_SELECTOR, '#sendOpsAlertEmailPopUp input[type="button"][value="Cancel"]'
        )
        cancel_btn.click()
        assert page.element_not_visible(*page.MODAL_SEND_OPS_EMAIL, timeout=10)

    def test_c339679_work_order_modal_close_button(self, driver):
        """C339679 work order modal: Verify Close button is working correctly."""
        page = _open_work_order(driver)
        page.find_visible(*page.WO_MODAL_WRAPPER, timeout=20)
        close_btn = page.find_visible(*page.WO_BTN_CLOSE, timeout=15)
        assert close_btn.is_displayed()
        assert "Close" in close_btn.text
        close_btn.click()
        assert page.element_not_visible(*page.WO_MODAL_WRAPPER, timeout=15)

    def test_c339680_work_order_modal_status_dropdown(self, driver):
        """C339680 work order modal: Status dropdown is visible and clickable."""
        page = _open_work_order(driver)
        # Native select exists and is enabled
        status_select = page.find_element(*page.WO_STATUS_SELECT, timeout=15)
        assert status_select.is_enabled()
        # Select2 rendered widget
        status_select2 = page.find_visible(*page.WO_STATUS_SELECT2, timeout=15)
        assert status_select2.is_displayed()
        # Open via Select2 jQuery API
        driver.execute_script("""
            var $sel = jQuery('#myWorkOrderView123 #ddlServiceHistoryStatus');
            $sel.select2('open');
        """)
        # Verify dropdown opened
        WebDriverWait(driver, 10).until(
            lambda d: "select2-container--open" in d.find_element(
                By.CSS_SELECTOR, "#myWorkOrderView123 #ddlServiceHistoryStatus + .select2-container"
            ).get_attribute("class")
        )
        # At least one option
        options = driver.find_elements(
            By.CSS_SELECTOR, "#myWorkOrderView123 .select2-results__option"
        )
        assert len(options) >= 1
        # Close
        driver.execute_script("""
            var $sel = jQuery('#myWorkOrderView123 #ddlServiceHistoryStatus');
            $sel.select2('close');
        """)
        WebDriverWait(driver, 10).until(
            lambda d: "select2-container--open" not in d.find_element(
                By.CSS_SELECTOR, "#myWorkOrderView123 #ddlServiceHistoryStatus + .select2-container"
            ).get_attribute("class")
        )
