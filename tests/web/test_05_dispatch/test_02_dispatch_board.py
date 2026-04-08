"""
Dispatch - Dispatch Board tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.dispatch_page import DispatchPage
from helpers.web_helper import wait_for_loading_screen


@pytest.mark.usefixtures("driver")
class TestDispatchBoard:
    """
    Verify Dispatch Board functionality: order info, filters, print, pin location,
    permanent schedule, and assigned orders.

    Usage:
        pytest tests/web/test_05_dispatch/test_02_dispatch_board.py -v
    """

    def _open_dispatch_board(self, driver):
        """Navigate to the Dispatch Board page."""
        page = DispatchPage(driver)
        page.navigate_to_dispatch_board()
        return page

    def _select_clairmont_route_and_search(self, page):
        """Common helper: open route filter, select Clairmont, and search."""
        page.open_route_filter()
        page.select_route_by_name("Clairmont")
        page.close_route_filter()
        page.click_board_search()

    # ── Tests ──────────────────────────────────────────────────────

    def test_c67611_order_info_displayed_and_add_notes_working(self, driver):
        """C67611 Order info displayed and add notes working."""
        page = self._open_dispatch_board(driver)
        self._select_clairmont_route_and_search(page)

        # Open the first work order
        page.click_first_work_order()

        # -- Tab 1: Order details -------------------------------------------
        page.click_work_order_tab(1)

        assert page.element_is_visible(*page.WO_TAB1_LOCATION), (
            "Location section should be visible on tab 1"
        )
        assert page.element_is_visible(*page.WO_TAB1_SERVICED), (
            "Serviced section should be visible on tab 1"
        )
        assert page.element_is_visible(*page.WO_TAB1_RECENTLY_VIEWED), (
            "Recently Viewed section should be visible on tab 1"
        )

        # Add a location note
        page.add_location_note("yes")

        # Add an operation response note
        page.add_operation_note("yes")

        # -- Tab 2 ----------------------------------------------------------
        page.click_work_order_tab(2)

        assert page.element_is_visible(*page.WO_TAB2_PANEL_CENTER), (
            "Panel center should be visible on tab 2"
        )
        assert page.element_is_visible(*page.WO_TAB2_LOCATION), (
            "Location should be visible on tab 2"
        )

        # -- Tab 3: Charges --------------------------------------------------
        page.click_work_order_tab(3)

        assert page.element_is_visible(*page.ADD_NEW_CHARGE_BTN), (
            "Add New Charge button should be visible on tab 3"
        )

        # Conditionally check disposal container
        if page.is_disposal_container_visible():
            assert page.element_is_visible(*page.ROUTE_TRIP_DISPOSAL_BTN), (
                "Disposal button should be visible when container is present"
            )

        # -- Tab 5: Attachments ----------------------------------------------
        page.click_work_order_tab(5)

        attachment_input = page.find_element(*page.ADD_ORDER_ATTACHMENT_FILE)
        assert attachment_input.is_enabled(), (
            "Attachment file input should be enabled on tab 5"
        )

        assert page.element_is_visible(*page.WO_TAB5_SIGNATURE_TEXT), (
            "Signature text should be visible on tab 5"
        )

        notes_span = page.find_visible(*page.WO_TAB5_NOTES_TEXT)
        assert notes_span.text == "yes", (
            f"Notes text should be 'yes', got '{notes_span.text}'"
        )

        # -- Tab 6 ----------------------------------------------------------
        page.click_work_order_tab(6)

        # -- Tab 10 ---------------------------------------------------------
        page.click_work_order_tab(10)

        # -- Tab 7 ----------------------------------------------------------
        page.click_work_order_tab(7)

    def test_c67612_dispatch_filter_is_working(self, driver):
        """C67612 Dispatch filter is working."""
        page = self._open_dispatch_board(driver)

        # Open region filter and check WA
        page.click_element(*page.HIDE_REGION_SPAN)

        wa_checkbox = page.find_clickable(*page.WA_CHECKBOX)
        if not wa_checkbox.is_selected():
            wa_checkbox.click()

        page.click_board_search()
        wait_for_loading_screen(driver)

        # Business Unit filter
        page.click_element(*page.BUSINESS_UNIT_FILTER_ARROW)
        page.click_element(*page.BU_SEGMENT_2ND)

        default_bu = page.find_clickable(*page.DEFAULT_BU_CHECKBOX)
        if not default_bu.is_selected():
            default_bu.click()

        page.click_element(*page.BU_SEGMENT_3RD)

        test_data = page.find_clickable(*page.TEST_DATA_CHECKBOX)
        if not test_data.is_selected():
            test_data.click()

        # Route filter - select all
        page.open_route_filter()
        page.click_element(*page.ROUTE_FILTER_SELECT_ALL)

        # Yard filter
        page.click_element(*page.YARD_FILTER_ARROW)
        yard_xpath = (
            "//li[contains(.,'Washington')]//input"
        )
        yard_cb = page.find_clickable(By.XPATH, yard_xpath)
        if not yard_cb.is_selected():
            page.driver.execute_script("arguments[0].click();", yard_cb)

        # Equipment type filter
        page.click_element(*page.EQUIPMENT_TYPE_FILTER_ARROW)
        page.click_element(*page.EQUIPMENT_TYPE_2ND)

        equip_cb = page.find_clickable(*page.EQUIPMENT_20YDRO)
        if not equip_cb.is_selected():
            equip_cb.click()

        # Supervisor filter (just open/close)
        page.click_element(*page.SUPERVISOR_FILTER_ARROW)

        # Order type filter
        page.click_element(*page.ORDER_TYPE_FILTER_ARROW)
        page.click_element(*page.ORDER_TYPE_2ND)

        end_svc = page.find_clickable(*page.END_SERVICE_CHECKBOX)
        if not end_svc.is_selected():
            end_svc.click()

        # Apply filters
        page.click_board_search()
        wait_for_loading_screen(driver)

        # Show all orders
        page.click_element(*page.FILTER_LABEL_SVG)

        show_all = page.find_clickable(*page.SHOW_ALL_ORDERS)
        if not show_all.is_selected():
            show_all.click()

        page.click_board_search()
        wait_for_loading_screen(driver)

        # Uncheck End Service order type
        page.click_element(*page.ORDER_TYPE_FILTER_ARROW)
        page.click_element(*page.ORDER_TYPE_2ND)

        end_svc = page.find_clickable(*page.END_SERVICE_CHECKBOX)
        if end_svc.is_selected():
            end_svc.click()

        # Uncheck WA region
        page.click_element(*page.MULTI_SEL_REGION)
        page.click_element(*page.REGION_LABEL_14TH)

        wa_checkbox = page.find_clickable(*page.WA_CHECKBOX)
        if wa_checkbox.is_selected():
            wa_checkbox.click()

        page.click_board_search()
        wait_for_loading_screen(driver)

        # Uncheck equipment type
        page.click_element(*page.MULTI_SEL_EQUIPMENT)
        page.click_element(*page.EQUIPMENT_TYPE_2ND)

        equip_cb = page.find_clickable(*page.EQUIPMENT_20YDRO)
        if equip_cb.is_selected():
            equip_cb.click()

        page.click_board_search()
        wait_for_loading_screen(driver)

    def test_c67613_print_functionality_working(self, driver):
        """C67613 Print functionality working."""
        page = self._open_dispatch_board(driver)
        self._select_clairmont_route_and_search(page)

        # Click print icon for route 101
        page.click_element(
            By.CSS_SELECTOR, "#printIcon_101 img.three-eye"
        )

        # Select print template
        page.select_print_template("409a0b20-8d51-4cc7-85f5-27409f714623")

        # Click the modal print button
        page.click_print_modal_btn()

    def test_c67614_pin_location_works(self, driver):
        """C67614 Pin Location works."""
        page = self._open_dispatch_board(driver)
        self._select_clairmont_route_and_search(page)

        # Store original window handle
        original_window = driver.current_window_handle

        # Open new tab
        driver.execute_script("window.open('about:blank','_blank');")
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        # Navigate back to the same dispatch board URL in the new tab
        from config.web_settings import BASE_URL
        driver.get(BASE_URL + "DispatchDashboard/DispatchBoard")
        wait_for_loading_screen(driver)

        # Click map icon for route 101
        page_new = DispatchPage(driver)
        page_new.click_element(*page_new.MAP_ICON_101)

        # Verify Dispatch Board Map page title
        title = page_new.get_page_title()
        assert "Dispatch Board Map" in title, (
            f"Page title should contain 'Dispatch Board Map', got '{title}'"
        )
        assert page_new.element_is_visible(*page_new.PAGE_TITLE), (
            "Page title should be visible"
        )

        # Verify map is visible
        assert page_new.element_is_visible(*page_new.BOARD_MAP_DIV), (
            "Map div should be visible"
        )

        # Switch back to original window
        driver.close()
        driver.switch_to.window(original_window)

    def test_c67615_apply_permanent_schedule(self, driver):
        """C67615 Apply Permanent Schedule."""
        page = self._open_dispatch_board(driver)

        # Select 'Automation test 2' route
        page.open_route_filter()
        page.select_route_by_name("Automation test 2")
        page.close_route_filter()
        page.click_board_search()

        # Click apply sequence icon
        page.click_apply_sequence_icon()

        # Verify modal content is visible
        assert page.element_is_visible(*page.SCHEDULE_UPDATE_MODAL_CONTENT), (
            "Schedule update modal content should be visible"
        )

        # Verify modal title
        modal_title = page.get_text(*page.SCHEDULE_UPDATE_MODAL_TITLE)
        assert modal_title == "Apply Current Route & Sequence to Permanent Schedule", (
            f"Modal title mismatch: '{modal_title}'"
        )
        assert page.element_is_visible(*page.SCHEDULE_UPDATE_MODAL_TITLE), (
            "Modal title should be visible"
        )

        # Verify PROCESS UPDATES button text and click it
        process_btn = page.find_visible(*page.PROCESS_UPDATES_BTN)
        assert process_btn.text == "PROCESS UPDATES", (
            f"Button text should be 'PROCESS UPDATES', got '{process_btn.text}'"
        )
        page.click_process_updates()

        # Wait for success message (up to 120 seconds as in Cypress)
        assert page.element_is_visible(*page.SUCCESS_MESSAGE, timeout=120), (
            "Success message should be visible after processing"
        )

        # Verify and click EXPORT LOG button
        export_btn = page.find_visible(*page.EXPORT_LOG_BTN)
        assert "EXPORT LOG" in export_btn.text, (
            f"Button text should contain 'EXPORT LOG', got '{export_btn.text}'"
        )
        page.click_export_log()

    def test_c67616_check_assigned_orders_plus_icon(self, driver):
        """C67616 Check Assigned Orders '+' icon."""
        page = self._open_dispatch_board(driver)
        self._select_clairmont_route_and_search(page)
        wait_for_loading_screen(driver)

        # Store original window handle
        original_window = driver.current_window_handle

        # Open new tab
        driver.execute_script("window.open('about:blank','_blank');")
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        # Navigate to the dispatch board in the new tab
        from config.web_settings import BASE_URL
        driver.get(BASE_URL + "DispatchDashboard/DispatchBoard")
        wait_for_loading_screen(driver)

        # Click expand icon for route 101
        page_new = DispatchPage(driver)
        page_new.click_element(By.CSS_SELECTOR, "#expandicon_101 svg")
        wait_for_loading_screen(driver)

        # Verify the Assigned Services title
        title_el = page_new.find_visible(*page_new.ASSIGNED_SERVICES_TITLE)
        assert "Assigned Services for" in title_el.text, (
            f"Title should contain 'Assigned Services for', got '{title_el.text}'"
        )
        assert page_new.element_is_visible(*page_new.ASSIGNED_SERVICES_TITLE), (
            "Assigned Services title should be visible"
        )

        # Switch back to original window
        driver.close()
        driver.switch_to.window(original_window)
