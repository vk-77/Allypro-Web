"""
Page object for the Elements Service pages.

Handles Update Service flow and Reassign Services operations.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .base_web_page import BaseWebPage
from config.web_settings import BASE_URL, DEFAULT_WAIT


class ServicePage(BaseWebPage):
    """
    Page object for Service-related operations:
    - Update Service wizard
    - Reassign Services page
    """

    # ── Customer Details / Service locators ─────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, "#content p.pageTitle")
    SERVICES_TAB = (By.ID, "center_li_1")
    UPDATE_SERVICE_BTN = (By.CSS_SELECTOR, 'a.btn-primary[onclick*="3,0,1"]')

    # Update Service wizard screens
    NEXT_SCREEN_2_BTN = (
        By.CSS_SELECTOR, 'input[onclick="GetNextUpdateServiceScreen2()"]'
    )
    FUTURE_DATED_MESSAGE = (By.ID, "divUpdateSvsMessage")
    DAY_OF_WEEK_SELECT_0 = (By.ID, "ddluDayofWeeek_0")
    ROUTE_SELECT2_CONTAINER_0 = (
        By.ID, "select2-ddluDayofRoute_0-container"
    )
    SEARCH_FIELD = (By.CSS_SELECTOR, '[class*="-search__field"]')
    NEXT_SCREEN_5_BTN = (
        By.CSS_SELECTOR, '[onclick="GetNextUpdateServiceScreen5()"]'
    )
    NEXT_SCREEN_6_BTN = (
        By.CSS_SELECTOR, '[onclick="GetNextUpdateServiceScreen6()"]'
    )
    ADD_ACTIVITY_CHECKBOX = (By.NAME, "chkAddActivity")
    ACTIVITY_TYPE_SELECT = (By.ID, "uService_DDlType")
    CONTACT_FIELD = (By.NAME, "uService_Contact")
    SUBMIT_UPDATE_BTN = (
        By.CSS_SELECTOR, '[onclick="return IsUpdateServiceFieldvalid()"]'
    )
    SUCCESS_MESSAGE_TEXT = "Service has been updated successfully."

    # ── Reassign Services locators ──────────────────────────────────
    REASSIGN_PAGE_TITLE = (By.CSS_SELECTOR, ".pageTitle")
    FILTER_LABEL = (By.CSS_SELECTOR, "#FilterLabel path")
    FILTER_LABEL_SVG = (By.CSS_SELECTOR, "#FilterLabel svg.svg_stroke")
    DIV_ROUTE = (By.ID, "divRoute")
    LOAD_BTN = (By.CSS_SELECTOR, "#reasign_routing_parent button.btn-primary")
    UPDATE_SEQUENCE_ONLY = (By.ID, "chkUpdateSequenceOnly")
    SEQUENCE_FIELDS = (By.CSS_SELECTOR, '[data-field="sequence"]')
    DAY_FIELDS = (By.CSS_SELECTOR, '[data-field="day"]')
    PROCESS_UPDATE_BTN = (By.CSS_SELECTOR, "#liProcessUpdate a.btn")
    CONFIRM_MODAL_TEXT = (
        By.CSS_SELECTOR, "#modalReassignServiceScheduleUpdate div.text-center"
    )
    CONFIRM_PROCESS_BTN = (By.ID, "btnReassignProcessUpdate")
    SUCCESS_CONTENT = (By.ID, "divSucessContent")

    # Reassign filter selectors
    FREQUENCY_CHECKBOX_FIRST = (
        By.CSS_SELECTOR,
        "#dispatchfilterContent div:nth-child(3) > "
        "div.dispatch-filter-content-inner > div.dispatch-filter-list > "
        "ul > li:nth-child(1) > label.checkbox",
    )
    FREQUENCY_INPUT_FIRST = (
        By.CSS_SELECTOR,
        "#dispatchfilterContent li:nth-child(1) input.checkbox_Frequency",
    )
    REASSIGN_STATUS_CHECKBOXES = (
        By.CSS_SELECTOR, '[data-type="clschkReassignStatus"]'
    )
    DAY_DROPDOWN_TOP = (By.ID, "DDlDayRRTop")
    ROUTE_SELECT2_TOP = (By.ID, "select2-DDlRouteRRTop-container")
    ROUTE_SEARCH_FIELD = (
        By.CSS_SELECTOR,
        "#EquipmentInventoryTable input.select2-search__field",
    )
    APPLY_DAY_ROUTE_BTN = (By.CSS_SELECTOR, "#divDisplayDayAndRoute input.btn")

    # ── Recently Viewed / Customer selection ────────────────────────
    RECENTLY_VIEWED_SECTION = (By.ID, "divRecentActivity")
    ADD_SERVICE_LINK = (By.CSS_SELECTOR, "a.AddNewServiceWizardLocation")
    ADD_SERVICE_MODAL = (By.ID, "myAddServiceLocationView")
    ADD_SERVICE_BODY = (By.ID, "AddServiceLocationBodyContainer")
    SERVICES_LIST = (By.ID, "services_list_container")

    # Add Service wizard selectors
    EQUIP_CATEGORY_SELECT = (By.ID, "Svc_EquipmentCategoryID")
    EQUIP_TYPE_SELECT2 = (
        By.CSS_SELECTOR, "#select2-Svc_EquipmentTypeID-container"
    )
    SERVICE_TYPE_SELECT2 = (
        By.CSS_SELECTOR, "#select2-Svc_ServiceTypeID-container"
    )
    FREQUENCY_TYPE_SELECT2 = (
        By.CSS_SELECTOR, "#select2-Svc_FrequencyTypeID-container"
    )
    OWNERSHIP_SELECT = (By.ID, "ddlSvc_OwnerShipID")
    ADD_SERVICE_ROUTING = (By.ID, "divAddServiceRoutingContainer")
    REQUESTED_BY = (By.ID, "Svc_RequestedBy")
    CHANGE_REASON_SELECT2 = (
        By.CSS_SELECTOR, "#select2-Svc_ServiceChangeReasonID-container"
    )
    NEW_SVC_CODE_SELECT2 = (By.CSS_SELECTOR, "#select2-NewSvcCode_1-container")
    ADD_CHARGE_BTN = (By.ID, "addUpdateNewCharge_1")
    ROUTE_WORKFLOW_SELECT2 = (
        By.CSS_SELECTOR,
        '[id^="select2-ddlDayRouteServiceCodeWorkflow_"][id$="-container"]',
    )
    SUBMIT_SERVICE_BTN = (
        By.CSS_SELECTOR, 'button[onclick="ShowTemporaryServicePopup()"]'
    )
    SERVICE_CREATED_TEXT = "Service has been created successfully."

    # ── Navigation helpers ──────────────────────────────────────────

    def select_recently_viewed_customer(self, customer_id):
        """
        Select a customer from Recently Viewed by ID.
        Falls back to clicking the first recently viewed link.
        """
        self.wait_for_loading_screen()
        try:
            self.find_visible(*self.RECENTLY_VIEWED_SECTION, timeout=10)
        except TimeoutException:
            pass

        # Try to find link by customer ID in onclick attribute
        try:
            link = self.find_clickable(
                By.CSS_SELECTOR,
                f'#divRecentActivity a[onclick*="{customer_id}"]',
                timeout=5,
            )
            link.click()
        except TimeoutException:
            # Fallback: click first recently viewed
            try:
                link = self.find_clickable(
                    By.CSS_SELECTOR,
                    "#divRecentActivity li:nth-child(1) a",
                    timeout=10,
                )
                link.click()
            except TimeoutException:
                # Last resort: navigate to customer details via URL
                self.driver.get(
                    BASE_URL + "CustomerDetails?cid=" + str(customer_id)
                )
        self.wait_for_loading_screen()

    def add_new_service_from_customer_details(self):
        """
        Run the Add New Service wizard from Customer Details.
        Mirrors Cypress addNewServiceFromCustomerDetails command.
        """
        wait = WebDriverWait(self.driver, 20)

        # Scroll to Services section and click Add Service link
        self.find_by_text("Services").click()
        try:
            link = self.find_clickable(
                By.CSS_SELECTOR, "a.AddNewServiceWizardLocation", timeout=5
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", link
            )
            self.driver.execute_script("arguments[0].click();", link)
        except TimeoutException:
            add_link = self.find_clickable(
                By.XPATH, "//a[contains(text(),'Add Service')]", timeout=10
            )
            self.driver.execute_script("arguments[0].click();", add_link)

        # Wait for modal
        modal = wait.until(
            EC.visibility_of_element_located(self.ADD_SERVICE_MODAL)
        )
        wait.until(EC.presence_of_element_located(self.ADD_SERVICE_BODY))

        # Equipment category (if visible)
        try:
            cat_el = self.driver.find_element(*self.EQUIP_CATEGORY_SELECT)
            if cat_el.is_displayed():
                Select(cat_el).select_by_visible_text("Recycler")
        except Exception:
            pass

        # Equipment type
        self._select2_in_modal(
            "#select2-Svc_EquipmentTypeID-container", "Norbert Recycler"
        )
        # Service type
        self._select2_in_modal(
            "#select2-Svc_ServiceTypeID-container", "BULK SERVICE"
        )
        # Frequency type
        self._select2_in_modal(
            "#select2-Svc_FrequencyTypeID-container", "5 days per week"
        )

        # Ownership (if present)
        try:
            own_el = self.driver.find_element(*self.OWNERSHIP_SELECT)
            if own_el.is_displayed():
                Select(own_el).select_by_index(1)
        except Exception:
            pass

        # Click Next twice
        self._click_visible_add_service_next()
        self._click_visible_add_service_next()

        # Routing: set day-of-week and route for 5 days
        self.find_visible(*self.ADD_SERVICE_ROUTING, timeout=10)
        for i in range(5):
            day_sel = self.find_visible(
                By.ID, f"ddlDayofWeeek_{i}", timeout=10
            )
            Select(day_sel).select_by_value(str(i + 1))
            self._select2_in_modal(
                f"#select2-ddlDayofRoute_{i}-container", "Automation test 1"
            )

        self._click_visible_add_service_next()

        # Click next on screen 4
        next4_btn = self.find_clickable(
            By.CSS_SELECTOR,
            'button[onclick*="ShowNextMyAddServiceLocationPopUp(4)"]',
            timeout=10,
        )
        next4_btn.click()

        # Requested By
        req_by = self.find_visible(*self.REQUESTED_BY, timeout=10)
        req_by.clear()
        req_by.send_keys("AutoMVC")

        # Change reason
        self._select2_in_modal(
            "#select2-Svc_ServiceChangeReasonID-container", "NEW CUST"
        )
        # Service code
        self._select2_in_modal("#select2-NewSvcCode_1-container", "DELFLAT")

        # Add charge
        self.click_element(*self.ADD_CHARGE_BTN)

        # Route workflow
        route_containers = self.driver.find_elements(
            *self.ROUTE_WORKFLOW_SELECT2
        )
        if route_containers:
            self._select2_in_modal(
                '[id^="select2-ddlDayRouteServiceCodeWorkflow_"]'
                '[id$="-container"]',
                "Automation test 1",
            )

        # Submit
        submit = self.find_clickable(*self.SUBMIT_SERVICE_BTN, timeout=10)
        submit.click()
        self.wait_for_loading_screen()

        # Verify created
        self.find_by_text(self.SERVICE_CREATED_TEXT, timeout=15)

        # Click last service in list
        self.find_visible(*self.SERVICES_LIST, timeout=10)
        service_items = self.driver.find_elements(
            By.CSS_SELECTOR, "#services_list_container li"
        )
        if service_items:
            last_item = service_items[-1]
            detail_link = last_item.find_elements(
                By.CSS_SELECTOR,
                'div[onclick*="CustomerDetailServiceInfoBoxPartial"]',
            )
            if detail_link:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    detail_link[0],
                )
                self.driver.execute_script(
                    "arguments[0].click();", detail_link[0]
                )

    def _select2_in_modal(self, container_css, search_text):
        """Select2 interaction within the Add Service modal."""
        wait = WebDriverWait(self.driver, 10)
        container = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f"#myAddServiceLocationView {container_css}")
        ))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", container
        )
        self.driver.execute_script("arguments[0].click();", container)

        try:
            search = wait.until(EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                ".select2-container--open input.select2-search__field",
            )))
            search.clear()
            search.send_keys(search_text + Keys.ENTER)
        except TimeoutException:
            option = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                f'//li[contains(@class,"select2-results__option") '
                f'and contains(text(),"{search_text}")]',
            )))
            option.click()

    def _click_visible_add_service_next(self):
        """Click the visible Next button in the Add Service modal footer."""
        wait = WebDriverWait(self.driver, 10)
        footers = self.driver.find_elements(
            By.CSS_SELECTOR, "#myAddServiceLocationView .myAddServiceBtnFooter"
        )
        for footer in footers:
            if footer.is_displayed():
                buttons = footer.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if "Next" in btn.text and btn.is_displayed():
                        btn.click()
                        return
        # Fallback
        btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//div[@id="myAddServiceLocationView"]'
            '//div[contains(@class,"myAddServiceBtnFooter")]'
            '//button[contains(text(),"Next")]',
        )))
        btn.click()

    # ── Update Service flow ─────────────────────────────────────────

    def verify_customer_details_title(self):
        """Verify page title contains 'Customer Details'."""
        title = self.find_visible(*self.PAGE_TITLE, timeout=10)
        assert "Customer Details" in title.text

    def click_services_tab(self):
        """Click the Services tab (center_li_1)."""
        self.click_element(*self.SERVICES_TAB)

    def click_update_service_button(self):
        """Click the Update Service button."""
        self.click_element(*self.UPDATE_SERVICE_BTN)
        self.wait_for_loading_screen()

    def click_next_screen_2(self):
        """Click Next on update service screen 1 -> screen 2."""
        btn = self.find_visible(*self.NEXT_SCREEN_2_BTN, timeout=10)
        btn.click()
        self.wait_for_loading_screen()

    def is_future_dated_message_visible(self):
        """Check if the future-dated changes message is visible."""
        try:
            el = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(self.FUTURE_DATED_MESSAGE)
            )
            return el.is_displayed()
        except TimeoutException:
            return False

    def get_future_dated_message_text(self):
        """Get text of the future-dated message div."""
        el = self.find_visible(*self.FUTURE_DATED_MESSAGE, timeout=10)
        return el.text

    def update_service_routing(self, day_value="3", route_search="car"):
        """Fill in the routing fields on the update service screen."""
        day_select = self.find_visible(*self.DAY_OF_WEEK_SELECT_0, timeout=10)
        Select(day_select).select_by_value(day_value)

        self.click_element(*self.ROUTE_SELECT2_CONTAINER_0)
        search = self.find_visible(*self.SEARCH_FIELD, timeout=10)
        search.send_keys(route_search + Keys.ENTER)

    def click_next_screen_5(self):
        """Click Next to screen 5."""
        self.click_element(*self.NEXT_SCREEN_5_BTN)
        self.wait_for_loading_screen()

    def click_next_screen_6(self):
        """Click Next to screen 6."""
        self.click_element(*self.NEXT_SCREEN_6_BTN)
        self.wait_for_loading_screen()

    def fill_activity_and_submit(
        self, activity_type="CUST W/CALL", contact="0785968548"
    ):
        """Check add activity, fill type/contact, and submit update."""
        checkbox = self.find_element(*self.ADD_ACTIVITY_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", checkbox)

        Select(
            self.find_visible(*self.ACTIVITY_TYPE_SELECT)
        ).select_by_visible_text(activity_type)

        contact_field = self.find_visible(*self.CONTACT_FIELD)
        contact_field.clear()
        contact_field.send_keys(contact)

        self.click_element(*self.SUBMIT_UPDATE_BTN)
        self.wait_for_loading_screen()

    def verify_update_success(self):
        """Verify the service updated successfully message."""
        assert self.text_is_visible(self.SUCCESS_MESSAGE_TEXT, timeout=15)

    # ── Reassign Services flow ──────────────────────────────────────

    def verify_reassign_page(self):
        """Verify we are on the Reassign Services page."""
        assert "/Operations/Reassign" in self.current_url()
        title = self.find_visible(*self.REASSIGN_PAGE_TITLE, timeout=10)
        assert "Reassign Services" in title.text

    def open_filter_panel(self):
        """Open the advanced filter panel."""
        self.click_element(*self.FILTER_LABEL_SVG)

    def close_filter_panel(self):
        """Close the advanced filter panel."""
        self.click_element(*self.FILTER_LABEL_SVG)

    def click_filter_label_path(self):
        """Click the filter label path icon to open filters."""
        self.driver.execute_script(
            "arguments[0].click();",
            self.find_element(*self.FILTER_LABEL),
        )

    def select_route_by_text(self, route_text):
        """Check a route checkbox by matching its label text (regex)."""
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        route_li = wait.until(EC.presence_of_element_located((
            By.XPATH,
            f'//div[@id="divRoute"]//li[contains(.,"{route_text}")]',
        )))
        checkbox = route_li.find_element(By.CSS_SELECTOR, "input.checkbox_Route")
        self.driver.execute_script("arguments[0].click();", checkbox)

    def select_route_label_by_index(self, index=2):
        """Click a route label by nth-child index."""
        selector = f"#divRoute li:nth-child({index}) label.checkbox"
        self.click_element(By.CSS_SELECTOR, selector)

    def check_route_checkbox_by_value(self, value):
        """Check a route checkbox by its value attribute."""
        cb = self.find_element(
            By.CSS_SELECTOR, f'#divRoute input[value="{value}"]'
        )
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)

    def click_frequency_first_label(self):
        """Click the first frequency checkbox label."""
        self.click_element(*self.FREQUENCY_CHECKBOX_FIRST)

    def check_frequency_first_input(self):
        """Check the first frequency input checkbox."""
        cb = self.find_element(*self.FREQUENCY_INPUT_FIRST)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)

    def check_frequency_by_value(self, value):
        """Check a frequency checkbox by value."""
        cb = self.find_element(
            By.CSS_SELECTOR,
            f'#dispatchfilterContent input[value="{value}"]',
        )
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)

    def click_load_button(self):
        """Click the Load / Search button on Reassign."""
        self.click_element(*self.LOAD_BTN)

    def check_update_sequence_only(self):
        """Check the Update Sequence Only checkbox."""
        cb = self.find_element(*self.UPDATE_SEQUENCE_ONLY)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)

    def type_sequence_in_first_enabled(self, value="24"):
        """Type a sequence value in the first enabled sequence field."""
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        fields = wait.until(lambda d: d.find_elements(*self.SEQUENCE_FIELDS))
        for field in fields:
            if field.is_enabled() and field.is_displayed():
                self.driver.execute_script("arguments[0].click();", field)
                field.clear()
                field.send_keys(value)
                return
        raise Exception("No enabled sequence field found")

    def select_day_in_first_enabled(self, index=2):
        """Select a day option in the first enabled day dropdown."""
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        fields = wait.until(lambda d: d.find_elements(*self.DAY_FIELDS))
        for field in fields:
            if field.is_enabled() and field.is_displayed():
                Select(field).select_by_index(index)
                return
        raise Exception("No enabled day field found")

    def check_reassign_status_checkbox(self, eq_index=1):
        """Check a reassign status checkbox by index (skipping disabled)."""
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        checkboxes = wait.until(
            lambda d: d.find_elements(*self.REASSIGN_STATUS_CHECKBOXES)
        )
        enabled = [cb for cb in checkboxes if cb.is_enabled()]
        if len(enabled) > eq_index:
            self.driver.execute_script(
                "arguments[0].click();", enabled[eq_index]
            )
        elif enabled:
            self.driver.execute_script("arguments[0].click();", enabled[0])

    def select_top_day_route(self, day_value="2", route_search="car"):
        """Select day and route in the top reassign bar."""
        Select(self.find_visible(*self.DAY_DROPDOWN_TOP)).select_by_value(
            day_value
        )
        self.click_element(*self.ROUTE_SELECT2_TOP)
        search = self.find_visible(*self.ROUTE_SEARCH_FIELD, timeout=10)
        search.clear()
        search.send_keys(route_search + Keys.ENTER)

    def click_apply_day_route(self):
        """Click the Apply button for day/route assignment."""
        self.click_element(*self.APPLY_DAY_ROUTE_BTN)
        self.wait_for_loading_screen()

    def click_process_update(self):
        """Click the Process Update button."""
        self.click_element(*self.PROCESS_UPDATE_BTN)

    def verify_confirmation_modal(self):
        """Verify the confirmation modal text."""
        text_el = self.find_visible(*self.CONFIRM_MODAL_TEXT, timeout=10)
        assert "Are you sure you want to process these Route Updates?" in text_el.text

    def click_confirm_process(self):
        """Click the confirm Process Update button in the modal."""
        btn = self.find_visible(*self.CONFIRM_PROCESS_BTN, timeout=10)
        btn.click()

    def verify_success_message(self):
        """Verify the success message after processing updates."""
        success = self.find_visible(*self.SUCCESS_CONTENT, timeout=15)
        assert "Update request is queued" in success.text
        assert success.is_displayed()
