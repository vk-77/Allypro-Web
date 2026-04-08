"""
Customer Details - Service Info widget tests.

"""
import pytest
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from pages.web.base_web_page import BaseWebPage
from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    scroll_to_element,
)
from data.user_data import USER_DATA


@pytest.mark.usefixtures("driver")
class TestServiceInfoWidget:
    """
    Service Info widget tests on Customer Details > Information tab.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_service_info_widget.py -v
    """

    def _expand_service_info(self, driver, page):
        """Expand the first Service Info block so detail fields are visible."""
        content = driver.find_element(By.ID, "content")
        services_el = content.find_element(By.XPATH, ".//*[contains(text(),'Services')]")
        scroll_to_element(driver, services_el)
        assert services_el.is_displayed()

        service_items = driver.find_elements(
            By.CSS_SELECTOR, "#services_list_container li:not(.no-services)"
        )
        if len(service_items) == 0:
            return

        heading = page.get_service_info_heading()
        if heading:
            scroll_to_element(driver, heading)
            driver.execute_script("arguments[0].click();", heading)
            WebDriverWait(driver, 6).until(lambda d: True)

    def test_c70539_service_info_heading_visible(self, driver):
        """C70539 Service Info heading is visible when customer has services."""
        page = CustomerPage(driver)

        page.add_new_service_from_customer_details()

        content = driver.find_element(By.ID, "content")
        services_el = content.find_element(By.XPATH, ".//*[contains(text(),'Services')]")
        scroll_to_element(driver, services_el)
        assert services_el.is_displayed()

        service_items = driver.find_elements(
            By.CSS_SELECTOR, "#services_list_container li:not(.no-services)"
        )
        if len(service_items) > 0:
            heading = page.get_service_info_heading()
            assert heading is not None, "Service Info heading should exist"
            scroll_to_element(driver, heading)
            assert heading.is_displayed(), "Service Info heading should be visible"

    def test_c70540_header_action_buttons_visible(self, driver):
        """C70540 Service Info - Verify header action buttons are visible when content is expanded."""
        page = CustomerPage(driver)

        page.select_and_click_first_service()

        service_items = driver.find_elements(
            By.CSS_SELECTOR, "#services_list_container li:not(.no-services)"
        )
        if len(service_items) == 0:
            return

        # Click heading to expand
        heading = page.get_service_info_heading()
        if heading:
            scroll_to_element(driver, heading)
            driver.execute_script("arguments[0].click();", heading)
            WebDriverWait(driver, 6).until(lambda d: True)

        # Get panel and check buttons
        panel = page._get_service_info_panel(heading)
        assert panel is not None, "Service Info panel should exist"

        # Add Order button
        add_order_btns = panel.find_elements(By.CSS_SELECTOR, "a.btn")
        add_order_found = any(
            re.search(r"Add\s*Order", btn.text, re.IGNORECASE) for btn in add_order_btns if btn.is_displayed()
        )
        assert add_order_found, "Add Order button should be visible"

        # Update button
        update_found = any(
            re.search(r"Update", btn.text, re.IGNORECASE) for btn in add_order_btns if btn.is_displayed()
        )
        assert update_found, "Update button should be visible"

        # Info icon
        info_icons = panel.find_elements(
            By.CSS_SELECTOR, 'a.servicemapicon.dropdown-toggle[data-toggle="dropdown"]'
        )
        assert any(i.is_displayed() for i in info_icons), "Info icon should be visible"

        # Hamburger button
        hamburger_btns = panel.find_elements(
            By.CSS_SELECTOR, "#dropdownMenuButton, span.al-humburgerIcon.dropdown-toggle"
        )
        assert any(h.is_displayed() for h in hamburger_btns), "Hamburger button should be visible"

    def test_c70541_equipment_view_history_modal(self, driver):
        """C70541 Service Info - Equipment View History modal displays details and closes correctly."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.select_and_click_first_service()

        content = driver.find_element(By.ID, "content")
        services_el = content.find_element(By.XPATH, ".//*[contains(text(),'Services')]")
        scroll_to_element(driver, services_el)

        service_items = driver.find_elements(
            By.CSS_SELECTOR, "#services_list_container li:not(.no-services)"
        )
        if len(service_items) == 0:
            return

        heading = page.get_service_info_heading()
        if heading:
            scroll_to_element(driver, heading)
            driver.execute_script("arguments[0].click();", heading)
            WebDriverWait(driver, 6).until(lambda d: True)

        # Click clock icon next to "Equipment" to open Equipment View History modal
        equip_headers = [
            h for h in content.find_elements(By.CSS_SELECTOR, "h4.serviceInfoEquipment")
            if h.is_displayed()
        ]
        assert len(equip_headers) > 0, "Equipment header should be visible"
        clock_icon = equip_headers[0].find_element(
            By.CSS_SELECTOR, 'a.servicemapicon[data-original-title="View History"]'
        )
        clock_icon.click()

        # Validate modal title
        label = wait.until(
            EC.visibility_of_element_located((By.ID, "myMapViewLabel"))
        )
        assert label.text == "Equipment View History"

        # Customer/location container
        cust_loc = driver.find_element(By.ID, "divCustLocContainer")
        assert cust_loc.is_displayed()

        cust_name = driver.find_element(By.ID, "settingsCustName")
        assert cust_name.is_displayed()
        assert cust_name.text.strip() != ""

        cust_location = driver.find_element(By.ID, "settingsCustLocation")
        assert cust_location.is_displayed()
        assert cust_location.text.strip() != ""

        customer_id = str(USER_DATA.get("customer_id", ""))
        if customer_id:
            assert customer_id in cust_name.text
            assert customer_id in cust_location.text

        # History container and table
        popup = driver.find_element(By.ID, "HistoryMapPopupContainer")
        assert popup.is_displayed()

        equip_history = driver.find_element(By.ID, "divEquipmentServiceChangeHistory")
        assert equip_history.is_displayed()

        table = equip_history.find_element(By.CSS_SELECTOR, "table.table-bordered")
        assert table.is_displayed()

        # Column headers
        headers = equip_history.find_elements(By.CSS_SELECTOR, "thead th")
        header_texts = [h.text for h in headers]
        for expected in ["Serial #", "Equipment Type", "Move Date", "User", "Processed"]:
            assert any(expected in ht for ht in header_texts), (
                f"Header '{expected}' not found in equipment history table"
            )

        # Close modal
        close_btn = driver.find_element(By.ID, "btnServicePopupClose")
        assert close_btn.is_displayed()
        assert "Close" in close_btn.text
        close_btn.click()

        # Verify modal is closed
        visible_labels = [
            el for el in driver.find_elements(By.ID, "myMapViewLabel")
            if el.is_displayed()
        ]
        assert len(visible_labels) == 0, "Modal should be closed"

    def test_c70542_service_started_billed_through_status_labels(self, driver):
        """C70542 Service Info - Displays Service, Started, Billed Through, and Status labels."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        detail_list = self._get_visible_service_details_list(driver)
        if detail_list is None:
            return

        for label_text in ["Service", "Started", "Billed Through", "Status"]:
            labels = detail_list.find_elements(
                By.XPATH, f".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'{label_text}')]"
            )
            visible = [l for l in labels if l.is_displayed()]
            assert len(visible) > 0, f"Label '{label_text}' should be visible"

    def test_c70543_service_rate_rental_rate_surcharges_labels(self, driver):
        """C70543 Service Info - Displays Service Rate, Rental Rate, Surcharges labels."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        detail_list = self._get_visible_service_details_list(driver)
        if detail_list is None:
            return

        for label_text in ["Service Rate", "Rental Rate"]:
            labels = detail_list.find_elements(
                By.XPATH, f".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'{label_text}')]"
            )
            visible = [l for l in labels if l.is_displayed()]
            assert len(visible) > 0, f"Label '{label_text}' should be visible"

        # Surcharges may have a dynamic suffix
        surcharge_labels = detail_list.find_elements(
            By.XPATH, ".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'Surcharges')]"
        )
        visible_surcharge = [l for l in surcharge_labels if l.is_displayed()]
        assert len(visible_surcharge) > 0, "Surcharges label should be visible"

    def test_c70544_frequency_type_ownership_labels(self, driver):
        """C70544 Service Info - Displays Frequency, Type, Ownership labels."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        detail_list = self._get_visible_service_details_list(driver)
        if detail_list is None:
            return

        for label_text in ["Frequency", "Type", "Ownership"]:
            labels = detail_list.find_elements(
                By.XPATH, f".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'{label_text}')]"
            )
            visible = [l for l in labels if l.is_displayed()]
            assert len(visible) > 0, f"Label '{label_text}' should be visible"

    def test_c70545_last_change_po_service_note_labels(self, driver):
        """C70545 Service Info - Displays Last Change, P.O. #, and Service Note labels."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        detail_list = self._get_visible_service_details_list(driver)
        if detail_list is None:
            return

        # Last Change
        lc_labels = detail_list.find_elements(
            By.XPATH, ".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'Last Change')]"
        )
        assert any(l.is_displayed() for l in lc_labels), "Last Change label should be visible"

        # P.O.# (uses label.cardLabel, not necessarily innerCard-Title)
        po_labels = detail_list.find_elements(
            By.XPATH, ".//label[contains(@class,'cardLabel') and contains(text(),'P.O.#')]"
        )
        assert any(l.is_displayed() for l in po_labels), "P.O.# label should be visible"

        # Service Note
        sn_labels = detail_list.find_elements(
            By.XPATH, ".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'Service Note')]"
        )
        assert any(l.is_displayed() for l in sn_labels), "Service Note label should be visible"

    def test_c70546_weekly_schedule_table_headers(self, driver):
        """C70546 Service Info - Weekly schedule table displays Monday-Sunday headers."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        content = driver.find_element(By.ID, "content")
        schedule_tables = [
            t for t in content.find_elements(By.CSS_SELECTOR, "table.route-table-schedule")
            if t.is_displayed()
        ]
        assert len(schedule_tables) > 0, "Schedule table should be visible"

        headers = schedule_tables[0].find_elements(By.CSS_SELECTOR, "thead th")
        header_texts = [h.text for h in headers]
        for day in ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            assert any(day in ht for ht in header_texts), (
                f"Day header '{day}' not found in schedule table"
            )

    def test_c70547_equipment_section_header(self, driver):
        """C70547 Service Info displays Equipment section header."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        content = driver.find_element(By.ID, "content")
        equip_headers = [
            h for h in content.find_elements(By.CSS_SELECTOR, "h4.serviceInfoEquipment")
            if h.is_displayed()
        ]
        assert len(equip_headers) > 0, "Equipment section header should be visible"
        assert any("Equipment" in h.text for h in equip_headers), (
            "Equipment section should contain 'Equipment' text"
        )

    def test_c70548_equipment_fields_equip_type_serial_holes_date(self, driver):
        """C70548 Service Info Equipment section displays Equip Type, Serial #, Holes #, Date on Site labels."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        content = driver.find_element(By.ID, "content")
        equip_sections = [
            s for s in content.find_elements(
                By.CSS_SELECTOR, "#divSingleEquipmentView, .equipment-service-detail"
            ) if s.is_displayed()
        ]
        assert len(equip_sections) > 0, "Equipment section should be visible"
        section = equip_sections[0]

        for label_text in ["Equip Type", "Serial #", "Holes #", "Date on Site"]:
            labels = section.find_elements(
                By.XPATH, f".//label[contains(text(),'{label_text}')]"
            )
            visible = [l for l in labels if l.is_displayed()]
            assert len(visible) > 0, f"Label '{label_text}' should be visible"

    def test_c70549_equipment_options_and_tag_labels(self, driver):
        """C70549 Service Info - Equipment section displays Equip Options and Tag # labels when present."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        content = driver.find_element(By.ID, "content")
        equip_sections = [
            s for s in content.find_elements(
                By.CSS_SELECTOR, "#divSingleEquipmentView, .equipment-service-detail"
            ) if s.is_displayed()
        ]
        if not equip_sections:
            return

        section = equip_sections[0]
        all_labels = section.find_elements(By.CSS_SELECTOR, "label")
        label_texts = [l.text for l in all_labels]

        has_equip_options_or_tag = any(
            re.search(r"Equip\s*Options|Tag\s*#", lt, re.IGNORECASE) for lt in label_texts
        )
        if has_equip_options_or_tag:
            matching = [
                l for l in all_labels
                if re.search(r"Equip\s*Options|Tag\s*#", l.text, re.IGNORECASE) and l.is_displayed()
            ]
            assert len(matching) > 0, "Equip Options or Tag # label should be visible when present"

    def test_c70550_card_label_content_for_service_and_started(self, driver):
        """C70550 Service Info - cardLabelContent displays values for Service and Started fields."""
        page = CustomerPage(driver)
        page.select_and_click_first_service()
        self._expand_service_info(driver, page)

        detail_list = self._get_visible_service_details_list(driver)
        if detail_list is None:
            return

        for label_text in ["Service", "Started"]:
            label_els = detail_list.find_elements(
                By.XPATH,
                f".//label[contains(@class,'innerCard-Title') and contains(@class,'cardLabel') and contains(text(),'{label_text}')]"
            )
            found_content = False
            for lbl in label_els:
                if lbl.is_displayed():
                    parent = lbl.find_element(By.XPATH, "./..")
                    contents = parent.find_elements(By.CSS_SELECTOR, ".cardLabelContent")
                    for c in contents:
                        if c.is_displayed():
                            found_content = True
                            break
                if found_content:
                    break
            assert found_content, f"cardLabelContent for '{label_text}' should exist and be visible"

    # ── Helpers ──

    def _get_visible_service_details_list(self, driver):
        """Return the first visible service details list element."""
        content = driver.find_element(By.ID, "content")
        lists = [
            el for el in content.find_elements(
                By.CSS_SELECTOR, "ul.service-detailsOuter.customerCardOuter"
            ) if el.is_displayed()
        ]
        return lists[0] if lists else None
