"""
Customer Details - Service Activity tab - work order Information tab.

"""
import re
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, force_click, scroll_to_element
from data.user_data import USER_DATA
from config.web_settings import DEFAULT_WAIT

ROUTE_REASSIGN_TARGET = "Automation test 2"


def _open_information_tab(driver):
    """Open today's work order and activate the Information tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_INFORMATION, page.WO_PANE_INFORMATION)
    return page


def _get_wo_modal_root(page):
    """Return the work order modal wrapper element."""
    return page.find_visible(*page.WO_MODAL_WRAPPER, timeout=20)


def _find_ops_results_panel(driver):
    """Find the Operations Results panel element."""
    section_title = driver.find_element(
        By.XPATH,
        '//*[contains(@class,"formSectionTitle") and contains(text(),"Operations Results")]'
    )
    return section_title.find_element(By.XPATH, './ancestor::*[contains(@class,"panel")][1]')


@pytest.mark.usefixtures("driver")
class TestModalInformationTab:
    """
    Service Activity tab - work order Information tab.

    """

    def test_c339683_information_tab_destination_priority_order_note(self, driver):
        """C339683 Information tab: Verify Destination, Priority, Order Note updates show success."""
        page = _open_information_tab(driver)
        modal = _get_wo_modal_root(page)

        # --- Destination ---
        dest_label = modal.find_element(By.XPATH, './/label[contains(text(),"Destination")]')
        assert dest_label.is_displayed()
        edit_btns = driver.find_elements(*page.WO_INFO_DESTINATION_EDIT)
        edit_btns[0].click()
        wait_for_loading_screen(driver)

        # Destination modal
        dest_modals = driver.find_elements(*page.WO_DESTINATION_MODAL)
        visible_modal = next((m for m in dest_modals if m.is_displayed()), None)
        assert visible_modal is not None
        title = visible_modal.find_element(By.CSS_SELECTOR, ".modal-title")
        assert "Update Destination" in title.text
        dest_select = page.find_visible(*page.WO_DESTINATION_SELECT)
        sel = Select(dest_select)
        sel.select_by_index(1)
        update_btn = page.find_visible(*page.WO_DESTINATION_UPDATE_BTN)
        update_btn.click()
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()

        # --- Priority ---
        modal = _get_wo_modal_root(page)
        body = page.find_visible(*page.WO_MODAL_BODY)
        priority_span = page.find_visible(*page.WO_PRIORITY_SPAN)
        priority_link = priority_span.find_element(*page.WO_PRIORITY_OPEN_LINK)
        assert priority_link.is_displayed()
        assert len(priority_link.text.strip()) > 0
        priority_link.click()
        wait_for_loading_screen(driver)

        # Priority modal
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                '//*[contains(@class,"modal-content") and contains(@class,"common")]'
                '//*[contains(@class,"modal-title") and contains(text(),"Update Priority")]'
            ))
        )
        priority_sel_el = page.find_visible(*page.WO_PRIORITY_SELECT)
        sel = Select(priority_sel_el)
        current_val = sel.first_selected_option.get_attribute("value") or ""
        next_val = "2" if current_val == "1" else "1"
        sel.select_by_value(next_val)
        update_btn = page.find_visible(*page.WO_PRIORITY_UPDATE_BTN)
        update_btn.click()
        wait_for_loading_screen(driver)
        page.assert_record_updated_success()

        # --- Order Note ---
        modal = _get_wo_modal_root(page)
        info_tab_link = page.find_visible(*page.WO_TAB_INFORMATION)
        info_tab_link.click()
        wait_for_loading_screen(driver)

        # ORDER NOTE section
        order_note_label = modal.find_element(
            By.XPATH, './/strong[contains(text(),"ORDER NOTE")]'
        )
        assert order_note_label.is_displayed()
        # Alert toggle
        alert_label = modal.find_element(
            By.XPATH, './/*[contains(@class,"order-note")]//descendant::*[contains(text(),"Alert")]'
        )
        assert alert_label.is_displayed()
        alert_toggle = page.find_element(*page.WO_ORDER_NOTE_ALERT_TOGGLE)
        assert alert_toggle.is_enabled()
        checked_before = alert_toggle.is_selected()
        force_click(driver, *page.WO_ORDER_NOTE_ALERT_TOGGLE)
        wait_for_loading_screen(driver)
        alert_toggle = page.find_element(*page.WO_ORDER_NOTE_ALERT_TOGGLE)
        assert alert_toggle.is_selected() != checked_before
        # Toggle back
        force_click(driver, *page.WO_ORDER_NOTE_ALERT_TOGGLE)
        wait_for_loading_screen(driver)
        alert_toggle = page.find_element(*page.WO_ORDER_NOTE_ALERT_TOGGLE)
        assert alert_toggle.is_selected() == checked_before

        # Edit note
        edit_links = driver.find_elements(*page.WO_ORDER_NOTE_EDIT_LINK)
        edit_links[0].click()
        wait_for_loading_screen(driver)
        textarea = page.find_visible(*page.WO_ORDER_NOTE_TEXTAREA, timeout=10)
        textarea.clear()
        textarea.send_keys(USER_DATA["automation_user"])
        save_btns = driver.find_elements(*page.WO_ORDER_NOTE_SAVE_BTN)
        visible_save = next((b for b in save_btns if b.is_displayed()), None)
        assert visible_save is not None
        visible_save.click()
        wait_for_loading_screen(driver)
        page.find_visible(*page.WO_MODAL_BODY)
        page.assert_record_updated_success()

    def test_c339674_information_tab_location_detail_and_map(self, driver):
        """C339674 Information tab: Location Detail fields and Scheduled Location map modal."""
        page = _open_information_tab(driver)
        modal = _get_wo_modal_root(page)

        # Location Detail section
        loc_section = modal.find_element(
            By.XPATH,
            './/*[contains(@class,"formSectionTitle") and contains(text(),"Location Detail")]'
        )
        panel = loc_section.find_element(By.XPATH, './ancestor::*[contains(@class,"panel")][1]')

        # SERVICE LOCATION label
        svc_loc = panel.find_element(By.XPATH, './/label[contains(text(),"SERVICE LOCATION")]')
        assert svc_loc.is_displayed()
        # Customer details link
        cust_link = panel.find_element(By.CSS_SELECTOR, 'a[href*="/CustomerDetails"]')
        assert cust_link.is_displayed()
        # Region
        region_label = panel.find_element(By.XPATH, './/label[contains(text(),"Region")]')
        assert region_label.is_displayed()
        # Tax Group
        tax_label = panel.find_element(By.XPATH, './/label[contains(text(),"Tax Group")]')
        assert tax_label.is_displayed()
        # Service Area
        sa_label = panel.find_element(By.XPATH, './/label[contains(text(),"Service Area")]')
        assert sa_label.is_displayed()
        # LOCATION PRIMARY CONTACT
        contact_label = panel.find_element(
            By.XPATH, './/label[contains(text(),"LOCATION PRIMARY CONTACT")]'
        )
        assert contact_label.is_displayed()

        # Click map link to open Scheduled Location modal
        map_links = panel.find_elements(*page.WO_LOCATION_DETAIL_MAP_LINK)
        map_links[0].click()
        wait_for_loading_screen(driver)

        # Verify Scheduled Location modal
        title_els = driver.find_elements(*page.WO_SCHEDULED_LOCATION_TITLE)
        visible_title = next((t for t in title_els if t.is_displayed()), None)
        assert visible_title is not None
        assert "Scheduled Location" in visible_title.text
        # Map canvas
        map_el = page.find_visible(*page.WO_SCHEDULED_LOCATION_MAP, timeout=20)
        assert map_el.is_displayed()
        # Close map modal
        modal_content = visible_title.find_element(
            By.XPATH, './ancestor::*[contains(@class,"modal-content") and contains(@class,"common")]'
        )
        close_btn = modal_content.find_element(
            By.CSS_SELECTOR, 'button.closeBtn[data-dismiss="modal"]'
        )
        close_btn.click()
        wait_for_loading_screen(driver)
        # Title should not be visible
        assert page.element_not_visible(*page.WO_SCHEDULED_LOCATION_TITLE, timeout=10)
        page.find_visible(*page.WO_MODAL_WRAPPER, timeout=10)

    def test_c339675_information_tab_operations_results(self, driver):
        """C339675 Information tab: Operations Results - route reassign, sequence, operations response."""
        page = _open_information_tab(driver)
        modal = _get_wo_modal_root(page)

        # Verify Operations Results panel fields
        ops_panel = _find_ops_results_panel(driver)
        # PERFORMED LOCATION label
        perf_label = ops_panel.find_element(
            By.XPATH, './/label[contains(text(),"PERFORMED LOCATION")]'
        )
        assert perf_label.is_displayed()
        # Type, Route, Sequence, Driver, Vehicle labels
        for label_text in ["Type", "Route", "Sequence", "Driver", "Vehicle"]:
            lbl = ops_panel.find_element(
                By.XPATH, f'.//label[contains(text(),"{label_text}")]'
            )
            assert lbl.is_displayed()
        # OPERATIONS RESPONSE
        ops_response = ops_panel.find_element(
            By.XPATH, './/strong[contains(text(),"OPERATIONS RESPONSE")]'
        )
        assert ops_response.is_displayed()

        # --- Route Reassign ---
        route_link = ops_panel.find_element(*page.WO_OPS_ROUTE_REASSIGN_LINK)
        route_link.click()
        wait_for_loading_screen(driver)
        # Reassign Route modal
        route_modal = page.find_visible(*page.WO_REASSIGN_ROUTE_MODAL, timeout=15)
        route_table = route_modal.find_element(By.CSS_SELECTOR, "table#tblRouteList")
        target_link = route_table.find_element(
            By.CSS_SELECTOR,
            f'a[onclick*="UpdateRouteInTableInfo(\'{ROUTE_REASSIGN_TARGET}\')"]'
        )
        scroll_to_element(driver, target_link)
        force_click(driver, By.CSS_SELECTOR,
                    f'a[onclick*="UpdateRouteInTableInfo(\'{ROUTE_REASSIGN_TARGET}\')"]')
        wait_for_loading_screen(driver)
        # Verify route updated
        WebDriverWait(driver, 25).until(
            lambda d: any(
                ROUTE_REASSIGN_TARGET in el.text
                for el in d.find_elements(*page.WO_OPS_ROUTE_CONTAINER)
                if el.is_displayed()
            ) or any(
                re.search(r"Route.*updated.*successfully", el.text, re.IGNORECASE)
                for el in d.find_elements(
                    By.CSS_SELECTOR, "#displayMsg, #msgBillAlert, #divSucessContent"
                )
                if el.text.strip()
            )
        )

        # --- Performed Location Map ---
        ops_panel = _find_ops_results_panel(driver)
        perf_map_link = ops_panel.find_element(*page.WO_PERFORMED_LOCATION_MAP_LINK)
        perf_map_link.click()
        wait_for_loading_screen(driver)
        title_els = driver.find_elements(*page.WO_SCHEDULED_LOCATION_TITLE)
        visible_title = next((t for t in title_els if t.is_displayed()), None)
        assert visible_title is not None
        assert "Scheduled Location" in visible_title.text
        map_el = page.find_visible(*page.WO_SCHEDULED_LOCATION_MAP, timeout=20)
        assert map_el.is_displayed()
        modal_content = visible_title.find_element(
            By.XPATH, './ancestor::*[contains(@class,"modal-content") and contains(@class,"common")]'
        )
        close_btn = modal_content.find_element(
            By.CSS_SELECTOR, 'button.closeBtn[data-dismiss="modal"]'
        )
        close_btn.click()
        wait_for_loading_screen(driver)

        # --- Sequence Modal ---
        ops_panel = _find_ops_results_panel(driver)
        seq_link = ops_panel.find_element(*page.WO_OPS_SEQUENCE_LINK)
        seq_link.click()
        wait_for_loading_screen(driver)
        heading_els = driver.find_elements(*page.WO_SEQUENCE_MODAL_HEADING)
        visible_heading = next((h for h in heading_els if h.is_displayed()), None)
        assert visible_heading is not None
        assert "Sequence" in visible_heading.text
        modal_content = visible_heading.find_element(
            By.XPATH, './ancestor::*[contains(@class,"modal-content")]'
        )
        route_input = modal_content.find_element(*page.WO_SEQUENCE_ROUTE_INPUT)
        assert route_input.is_displayed()
        eta_input = modal_content.find_element(*page.WO_SEQUENCE_ETA_INPUT)
        eta_input.click()
        eta_input.clear()
        eta_input.send_keys("8:00 AM")
        update_btn = modal_content.find_element(*page.WO_SEQUENCE_UPDATE_BTN)
        update_btn.click()
        wait_for_loading_screen(driver)
        # Verify ETA widget updated
        ops_panel = _find_ops_results_panel(driver)
        eta_widget = ops_panel.find_element(*page.WO_OPS_ETA_WIDGET)
        WebDriverWait(driver, 15).until(
            lambda d: re.search(r"8:00|08:00", eta_widget.text.strip().lower())
        )

        # --- Operations Response Edit ---
        ops_panel = _find_ops_results_panel(driver)
        edit_link = ops_panel.find_element(*page.WO_OPS_RESPONSE_EDIT_LINK)
        edit_link.click()
        wait_for_loading_screen(driver)
        ops_panel = _find_ops_results_panel(driver)
        textarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(page.WO_OPS_RESPONSE_TEXTAREA)
        )
        textarea.clear()
        textarea.send_keys(USER_DATA["assigned_user"])
        save_btns = ops_panel.find_elements(*page.WO_OPS_RESPONSE_SAVE_BTN)
        visible_save = next((b for b in save_btns if b.is_displayed()), None)
        assert visible_save is not None
        visible_save.click()
        wait_for_loading_screen(driver)
        # Verify response display
        ops_panel = _find_ops_results_panel(driver)
        response_span = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(page.WO_OPS_RESPONSE_DISPLAY)
        )
        assert USER_DATA["assigned_user"] in response_span.text
