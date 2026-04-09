"""
Customer Details page object and all sub-section helpers.

Covers tab navigation (Contacts, Service Activity, Account Activity,
Transactions, Audit, Documents, Pricing), Customer Settings, the
Services list, Service Info panels, Add Service wizard, and the
Service Activity calendar / work-order modal interactions.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .base_web_page import BasePage
from config.web_settings import BASE_URL


class CustomerPage(BasePage):
    """Page object for Customer Details and all sub-sections."""

    # ── Locators ──────────────────────────────────────────────────

    CUSTOMER_NAME = (By.CSS_SELECTOR, "#spnCustomerName, .customerName")
    RECENTLY_VIEWED_SECTION = (By.ID, "divRecentActivity")
    RECENTLY_VIEWED_FIRST_LINK = (By.CSS_SELECTOR, "#divRecentActivity li:nth-child(1) a")

    # Dashboard action buttons
    ADD_PAYMENT_BTN = (By.CSS_SELECTOR, '[data-original-title="Add Payment"]')
    ADD_ADJUSTMENT_BTN = (By.CSS_SELECTOR, '[onclick="ShowAddAdjustmentPopup(1)"]')
    CREATE_INVOICE_BTN = (By.CSS_SELECTOR, '[onclick="checkBillingBatchExist()"]')
    ADD_ACTIVITY_BTN = (By.CSS_SELECTOR, '[onclick="CTabActivityNotePopUp(1)"]')
    VIEW_SERVICES_BTN = (By.CSS_SELECTOR, '[onclick="ShowCustomerAllServices()"]')
    GENERATE_REPORT_BTN = (By.CSS_SELECTOR, '[onclick="ShowGenerateCustomerReportPopUp()"]')
    FLAG_CONTAINER = (By.ID, "customerFlagContainer")

    # Tab locators
    CONTACTS_TAB = (By.CSS_SELECTOR, '[onclick="ContactDetailAllTabActive(2)"]')
    SERVICE_ACTIVITY_TAB = (By.CSS_SELECTOR, '[onclick="ContactDetailAllTabActive(3)"]')
    ACCOUNT_ACTIVITY_TAB = (By.CSS_SELECTOR, '[onclick="ContactDetailAllTabActive(4)"]')
    TRANSACTIONS_TAB = (By.CSS_SELECTOR, '#parentLiTab_5 a, a[aria-controls="billing-history"]')
    AUDIT_TAB = (By.CSS_SELECTOR, '[onclick="ContactDetailAllTabActive(6)"]')
    DOCUMENTS_TAB = (By.CSS_SELECTOR, '[onclick="ContactDetailAllTabActive(7)"]')
    PRICING_TAB = (By.CSS_SELECTOR, '[onclick="ContactDetailAllTabActive(8)"]')

    # Tab panes
    CONTACTS_PANE = (By.CSS_SELECTOR, "#parentTabContainer_2.tab-pane.active")
    SERVICE_ACTIVITY_PANE = (By.CSS_SELECTOR, "#parentTabContainer_3.tab-pane.active")
    ACCOUNT_ACTIVITY_PANE = (By.CSS_SELECTOR, "#parentTabContainer_4.tab-pane.active")

    # Customer Settings
    CUSTOMER_SETTINGS_LABEL = "Customer Settings"
    CUSTOMER_SETTINGS_DROPDOWN = (
        By.CSS_SELECTOR,
        "#content .customer-setting .cardHeader-Wrap .dropdown-toggle",
    )
    CUSTOMER_SETTINGS_OPTIONS = (
        By.CSS_SELECTOR,
        "#content .customer-setting .dropdownOuter-Options",
    )

    # User preferences
    USER_IMAGE = (By.CSS_SELECTOR, "#content span.userImage img")
    USER_PREFERENCES_LINK = (By.CSS_SELECTOR, "#mySidebaruser p.al-userPrefrences")
    HOME_SCREEN_MIDDLE_SELECT = (By.ID, "ddlHomeScreenMiddle")

    # Information tab
    SERVICE_LOCATION_ID_FIELD = (By.ID, "InformationTabInfo_ServiceLocationIDDash")

    # ── Contacts tab locators ─────────────────────────────────────
    CONTACTS_TAB_PANE = (By.ID, "parentTabContainer_2")
    CONTACTS_ADD_BTN = (
        By.CSS_SELECTOR,
        '#parentTabContainer_2 a.btn.btn-primary[onclick="ShowCTab(1)"]',
    )
    CONTACTS_DELETE_BTN = (By.ID, "btnCTabMultipleDelete")
    CONTACTS_STATUS_FILTER = (By.ID, "contactStatusFilter")
    CONTACTS_LOCATION_FILTER = (By.ID, "contactServiceFilter")
    CONTACTS_GRID = (By.ID, "contactsDataGridContainer")
    CONTACTS_GRID_DX = (By.CSS_SELECTOR, "#contactsDataGridContainer .dx-datagrid")
    CONTACTS_GROUP_PANEL = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-datagrid-group-panel",
    )
    CONTACTS_SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-datagrid-search-panel input",
    )
    CONTACTS_DATA_ROWS = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-data-row",
    )
    CONTACTS_FIELD_SELECTOR_BTN = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer [aria-label='Field Selector'],"
        " #contactsDataGridContainer .dx-datagrid-column-chooser-button",
    )
    CONTACTS_GRID_SCROLLABLE = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-scrollable-container",
    )
    CONTACTS_EDIT_LINK = (
        By.CSS_SELECTOR,
        '#parentTabContainer_2 a[onclick*="editContactCTab"]',
    )
    CONTACTS_DELETE_LINK = (
        By.CSS_SELECTOR,
        '#parentTabContainer_2 a.deleteBtn[onclick*="deleteCustomerContactFromList"]',
    )
    CONTACTS_PAGER = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-datagrid-pager",
    )
    CONTACTS_PAGE_SIZES = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-datagrid-pager .dx-page-sizes",
    )
    CONTACTS_FILTER_PANEL_TEXT = (
        By.CSS_SELECTOR,
        "#contactsDataGridContainer .dx-datagrid-filter-panel-text",
    )

    # Edit Contact popup
    EDIT_CONTACT_POPUP = (
        By.CSS_SELECTOR,
        '#addEditContactPopupContainer, [id*="addEditContact"]',
    )
    EDIT_CONTACT_COMPANY = (By.ID, "Svc_CTabCompany")
    EDIT_CONTACT_TYPE = (By.ID, "Svc_ContactTypeId")
    EDIT_CONTACT_LOCATION = (By.ID, "Svc_ActivityServiceLocationUID")
    EDIT_CONTACT_ADD_DETAIL_LINK = (
        By.CSS_SELECTOR,
        'a[onclick="ShowContactSaveRow()"]',
    )
    EDIT_CONTACT_DETAIL_TYPE = (By.ID, "ddlCTabDetailType")
    EDIT_CONTACT_DETAIL_PHONE = (By.ID, "txtCTabDetailPhone")
    EDIT_CONTACT_PRIORITY = (By.ID, "ddlCTabPriority")
    EDIT_CONTACT_SAVE_DETAIL_BTN = (
        By.CSS_SELECTOR,
        'button[onclick="AddCTabCustDetail()"], .btnSave[title="Save"]',
    )
    EDIT_CONTACT_SAVE_BTN = (By.ID, "btnCTab")

    # ── Navigation ────────────────────────────────────────────────

    def open_customer_details_page(self):
        """Navigate to Customer Details via Recently Viewed, with URL fallback."""
        self.driver.get(BASE_URL)
        self.wait_for_loading_screen()
        self._ensure_recently_viewed_visible()

        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.RECENTLY_VIEWED_FIRST_LINK)
            )
            link.click()
            self.wait_for_loading_screen()
            WebDriverWait(self.driver, 15).until(
                lambda d: "/CustomerDetails" in d.current_url
            )
        except TimeoutException:
            self._load_customer_by_search()

    def _ensure_recently_viewed_visible(self):
        """Ensure the Recently Viewed section is visible on the home page."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.RECENTLY_VIEWED_SECTION)
            )
        except TimeoutException:
            pass

    def _load_customer_by_search(self):
        """Fallback: navigate to Customer Details via URL."""
        from data.user_data import USER_DATA
        self.driver.get(BASE_URL)
        self.wait_for_loading_screen()
        try:
            link = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 'a[href*="/CustomerDetails"]'
                ))
            )
            link.click()
            self.wait_for_loading_screen()
        except TimeoutException:
            pass

    def is_customer_details_loaded(self):
        """Return True if customer details page is loaded."""
        return "/CustomerDetails" in self.current_url()

    def get_customer_name(self):
        """Return the displayed customer name."""
        return self.get_text(*self.CUSTOMER_NAME, timeout=15)

    # ── Tab navigation ────────────────────────────────────────────

    def open_contacts_tab(self):
        """Open the Contacts tab."""
        elements = self.find_elements(*self.CONTACTS_TAB)
        elements[-1].click()
        self.wait_for_loading_screen()
        self.find_visible(*self.CONTACTS_PANE, timeout=10)

    def open_service_activity_tab(self):
        """Open the Service Activity tab."""
        elements = self.find_elements(*self.SERVICE_ACTIVITY_TAB)
        elements[-1].click()
        self.wait_for_loading_screen()
        self.find_visible(*self.SERVICE_ACTIVITY_PANE, timeout=10)

    def open_account_activity_tab(self):
        """Open the Account Activity tab."""
        elements = self.find_elements(*self.ACCOUNT_ACTIVITY_TAB)
        elements[-1].click()
        self.wait_for_loading_screen()
        self.find_visible(*self.ACCOUNT_ACTIVITY_PANE, timeout=10)

    def open_transactions_tab(self):
        """Open the Transactions tab."""
        el = self.find_visible(*self.TRANSACTIONS_TAB)
        el.click()
        self.wait_for_loading_screen()

    def open_audit_tab(self):
        """Open the Audit tab."""
        elements = self.find_elements(*self.AUDIT_TAB)
        elements[-1].click()
        self.wait_for_loading_screen()

    def open_documents_tab(self):
        """Open the Documents & Plans tab."""
        elements = self.find_elements(*self.DOCUMENTS_TAB)
        elements[-1].click()
        self.wait_for_loading_screen()

    def open_pricing_tab(self):
        """Open the Pricing tab."""
        elements = self.find_elements(*self.PRICING_TAB)
        elements[-1].click()
        self.wait_for_loading_screen()

    # ── Customer Settings ─────────────────────────────────────────

    def open_customer_settings_menu(self, option_name=None):
        """
        Open the Customer Settings card dropdown.
        Optionally click a menu option.
        """
        self.find_by_text(self.CUSTOMER_SETTINGS_LABEL).click()
        self.click_element(*self.CUSTOMER_SETTINGS_DROPDOWN)
        self.find_visible(*self.CUSTOMER_SETTINGS_OPTIONS)

        if option_name:
            option = self.find_clickable(
                By.XPATH,
                f'//div[contains(@class,"dropdownOuter-Options")]//a[contains(text(),"{option_name}")]',
            )
            option.click()

    # ── Dashboard actions ─────────────────────────────────────────

    def click_add_payment(self):
        """Click the Add Payment button."""
        self.click_element(*self.ADD_PAYMENT_BTN)

    def click_add_adjustment(self):
        """Click the Add Adjustment button."""
        self.click_element(*self.ADD_ADJUSTMENT_BTN)
        self.wait_for_loading_screen()

    def click_create_invoice(self):
        """Click the Create Invoice button."""
        self.click_element(*self.CREATE_INVOICE_BTN)
        self.wait_for_loading_screen()

    def click_add_activity(self):
        """Click the Add Activity button."""
        elements = self.find_elements(*self.ADD_ACTIVITY_BTN)
        elements[0].click()
        self.wait_for_loading_screen()

    def click_view_services(self):
        """Click the View Services button."""
        elements = self.find_elements(*self.VIEW_SERVICES_BTN)
        elements[0].click()
        self.wait_for_loading_screen()

    def click_generate_report(self):
        """Click the Generate Report button."""
        self.click_element(*self.GENERATE_REPORT_BTN)
        self.wait_for_loading_screen()

    def click_flags(self):
        """Click the flags container."""
        self.click_element(*self.FLAG_CONTAINER)
        self.wait_for_loading_screen()

    # ── Contacts tab helpers ──────────────────────────────────────

    def scroll_contacts_grid_right(self):
        """Scroll the contacts data grid to the right to reveal Action column."""
        container = self.find_element(*self.CONTACTS_GRID_SCROLLABLE)
        self.driver.execute_script(
            "arguments[0].scrollLeft = arguments[0].scrollWidth;", container
        )

    def get_contacts_column_header(self, label_fragment):
        """Return a column header element whose aria-label contains *label_fragment*."""
        selector = (
            f'#contactsDataGridContainer [role="columnheader"]'
            f'[aria-label*="{label_fragment}"]'
        )
        return self.find_element(By.CSS_SELECTOR, selector, timeout=10)

    def contacts_column_header_exists(self, label_fragment, timeout=10):
        """Return True if a column header with *label_fragment* exists."""
        selector = (
            f'#contactsDataGridContainer [role="columnheader"]'
            f'[aria-label*="{label_fragment}"]'
        )
        return self.element_exists(By.CSS_SELECTOR, selector, timeout=timeout)

    def contacts_column_header_not_present(self, label_fragment, timeout=5):
        """Return True if a column header with *label_fragment* is absent."""
        selector = (
            f'#contactsDataGridContainer [role="columnheader"]'
            f'[aria-label*="{label_fragment}"]'
        )
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except TimeoutException:
            return False

    # ── Service Info helpers ──────────────────────────────────────

    # Service list selectors
    SERVICES_LIST_CONTAINER = (By.ID, "services_list_container")
    SERVICE_ITEM_LINK = "div[onclick*='CustomerDetailServiceInfoBoxPartial']"
    FIRST_SERVICE_CHECKBOX = ".service_infochkbox input.chkAddServiceLocationForOrder"
    SERVICE_INFO_HEADING_CSS = ".innerContentTitle, h3, [class*='service-info-heading']"
    PANEL_PARENT_CSS = ".card, .panel, .cardOuterWrap, [class*='panel']"
    HAMBURGER_BTN_CSS = "#dropdownMenuButton, span.al-humburgerIcon.dropdown-toggle"
    DROPDOWN_MENU_CSS = ".dropdown-menu.dropdownOuter-Options, .dropdownOuter-Options, .dropdown-menu"

    # Add Service modal
    ADD_SERVICE_MODAL = (By.ID, "myAddServiceLocationView")
    ADD_SERVICE_BODY = (By.ID, "AddServiceLocationBodyContainer")

    def _has_service_items(self):
        """Return True if there are service items in the services list."""
        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#services_list_container li:not(.no-services)"
        )
        return len(items) > 0

    def select_first_service(self):
        """Click the first service item in the services list."""
        self.find_by_text("Services", tag="*", timeout=10)
        self.find_visible(*self.SERVICES_LIST_CONTAINER, timeout=10)
        if not self._has_service_items():
            return
        item = self.driver.find_element(
            By.CSS_SELECTOR,
            f"#services_list_container li:not(.no-services) {self.SERVICE_ITEM_LINK}"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", item)
        self.driver.execute_script("arguments[0].click();", item)

    def select_last_service(self):
        """Click the last service item in the services list."""
        self.find_by_text("Services", tag="*", timeout=10)
        self.find_visible(*self.SERVICES_LIST_CONTAINER, timeout=10)
        if not self._has_service_items():
            return
        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            f"#services_list_container li:not(.no-services) {self.SERVICE_ITEM_LINK}"
        )
        last = items[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", last)
        self.driver.execute_script("arguments[0].click();", last)

    def select_and_click_first_service(self):
        """Check the first service checkbox and click the service item."""
        self.find_by_text("Services", tag="*", timeout=10)
        self.find_visible(*self.SERVICES_LIST_CONTAINER, timeout=10)
        if not self._has_service_items():
            return
        first_li = self.driver.find_element(
            By.CSS_SELECTOR, "#services_list_container li:not(.no-services)"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_li)
        chk = first_li.find_element(By.CSS_SELECTOR, self.FIRST_SERVICE_CHECKBOX)
        if not chk.is_selected():
            self.driver.execute_script("arguments[0].click();", chk)
        link = first_li.find_element(By.CSS_SELECTOR, self.SERVICE_ITEM_LINK)
        self.driver.execute_script("arguments[0].click();", link)

    def _find_service_info_headings(self):
        """Return all Service Info heading elements matching the pattern."""
        headings = self.driver.find_elements(By.CSS_SELECTOR, self.SERVICE_INFO_HEADING_CSS)
        import re
        pattern = re.compile(r"Service\s*Info\s*\(\d+\)", re.IGNORECASE)
        return [h for h in headings if pattern.search(h.text)]

    def _get_service_info_panel(self, heading):
        """Return the panel parent element for a Service Info heading."""
        for sel in self.PANEL_PARENT_CSS.split(","):
            try:
                cls_name = sel.strip().lstrip(".")
                xpath = "./ancestor::*[contains(@class,'{}')]".format(cls_name)
                panel = heading.find_element(By.XPATH, xpath)
                return panel
            except NoSuchElementException:
                continue
        # Fallback: walk up via JS
        return self.driver.execute_script(
            """
            var el = arguments[0];
            var selectors = arguments[1].split(',');
            while (el) {
                for (var i = 0; i < selectors.length; i++) {
                    try { if (el.matches(selectors[i].trim())) return el; } catch(e) {}
                }
                el = el.parentElement;
            }
            return null;
            """,
            heading, self.PANEL_PARENT_CSS
        )

    def _open_hamburger_menu(self, panel):
        """Open the hamburger dropdown menu on a service info panel."""
        btn = panel.find_elements(By.CSS_SELECTOR, self.HAMBURGER_BTN_CSS)
        if btn:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn[0])
            self.driver.execute_script("arguments[0].click();", btn[0])
            WebDriverWait(self.driver, 10).until(
                lambda d: len([m for m in panel.find_elements(By.CSS_SELECTOR, self.DROPDOWN_MENU_CSS) if m.is_displayed()]) > 0
            )

    def _click_hamburger_option(self, panel, option_text):
        """Click a specific option from the visible hamburger dropdown menu."""
        menus = [m for m in panel.find_elements(By.CSS_SELECTOR, self.DROPDOWN_MENU_CSS) if m.is_displayed()]
        for menu in menus:
            links = menu.find_elements(By.CSS_SELECTOR, "a, [role='button']")
            for link in links:
                if option_text.lower() in link.text.lower():
                    self.driver.execute_script("arguments[0].click();", link)
                    return
        raise Exception(f"Menu option '{option_text}' not found in hamburger dropdown")

    def _run_service_info_menu_flow(self, service_index, menu_option, expected_modal_css, timeout=10):
        """
        Shared flow: expand service at index, open hamburger, click menu item, wait for modal.
        service_index: 0 (first), 1 (second), or 'last'
        """
        from helpers.web_helper import wait_for_loading_screen as _wfls

        self.find_by_text("Services", tag="*", timeout=10)
        self.find_visible(*self.SERVICES_LIST_CONTAINER, timeout=10)
        if not self._has_service_items():
            return

        # Click service at index
        items = self.driver.find_elements(
            By.CSS_SELECTOR,
            f"#services_list_container li:not(.no-services) {self.SERVICE_ITEM_LINK}"
        )
        if service_index == "last":
            target = items[-1]
        elif isinstance(service_index, int) and service_index < len(items):
            target = items[service_index]
        else:
            target = items[0]

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
        self.driver.execute_script("arguments[0].click();", target)
        WebDriverWait(self.driver, 6).until(
            lambda d: True  # brief pause for panel to expand
        )

        # Find and click the heading to ensure panel is expanded
        headings = self._find_service_info_headings()
        if service_index == "last":
            heading = headings[-1] if headings else None
        elif service_index == 1 and len(headings) > 1:
            heading = headings[0]
        else:
            heading = headings[0] if headings else None

        if heading:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", heading)
            if service_index == "last" or service_index == 1:
                self.driver.execute_script("arguments[0].click();", heading)

        # Get panel, open hamburger, click option
        panel = self._get_service_info_panel(heading)
        self._open_hamburger_menu(panel)
        self._click_hamburger_option(panel, menu_option)

        # Wait for expected modal
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, expected_modal_css))
        )

    def _close_popup_if_open(self, modal_css, close_btn_css):
        """Close a modal/popup if it is currently open."""
        try:
            modals = self.driver.find_elements(By.CSS_SELECTOR, modal_css)
            for modal in modals:
                if modal.is_displayed():
                    btns = modal.find_elements(By.CSS_SELECTOR, close_btn_css)
                    if btns:
                        self.driver.execute_script("arguments[0].click();", btns[0])
                        WebDriverWait(self.driver, 5).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, modal_css))
                        )
        except (TimeoutException, NoSuchElementException):
            pass

    def open_service_info_view_history(self):
        """Open View History from the first service's hamburger menu."""
        self._close_popup_if_open(
            "#commonHistoryMapPopup.in, #commonHistoryMapPopup.show",
            "#btnServicePopupClose"
        )
        self._run_service_info_menu_flow(0, "View History", "#divCustomerServiceChangeHistory")

    def open_service_info_update_routing(self):
        """Open Update Routing from the second service's hamburger menu."""
        self._close_popup_if_open(
            "#commonHistoryMapPopup.in, #commonHistoryMapPopup.show",
            "#btnServicePopupClose"
        )
        self._run_service_info_menu_flow(1, "Update Routing", "#reassignRoutingPopUpBody")

    def open_service_info_transfer_service(self):
        """Open Transfer Service from the first service's hamburger menu."""
        self._close_popup_if_open(
            "#commonHistoryMapPopup.in, #commonHistoryMapPopup.show",
            "#btnServicePopupClose"
        )
        self._close_popup_if_open(
            "#modalSerivceTransfer.in, #modalSerivceTransfer.show",
            "button.closeBtn, [onclick*='modalSerivceTransfer']"
        )
        self._run_service_info_menu_flow(0, "Transfer Service", "#modalSerivceTransfer")

    def open_service_info_transfer_service_for_last_service(self):
        """Open Transfer Service from the last service's hamburger menu."""
        self._close_popup_if_open(
            "#commonHistoryMapPopup.in, #commonHistoryMapPopup.show",
            "#btnServicePopupClose"
        )
        self._close_popup_if_open(
            "#modalSerivceTransfer.in, #modalSerivceTransfer.show",
            "button.closeBtn, [onclick*='modalSerivceTransfer']"
        )
        self._run_service_info_menu_flow("last", "Transfer Service", "#modalSerivceTransfer")

    def add_new_service_from_customer_details(self, requested_by=None):
        """Run the Add Service wizard to create a new service with default values."""
        from helpers.web_helper import wait_for_loading_screen as _wfls, select2_select
        from data.user_data import USER_DATA

        content = self.find_element(By.ID, "content")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            self.find_by_text("Services")
        )

        # Click Add Service link
        try:
            link = self.driver.find_element(By.CSS_SELECTOR, "a.AddNewServiceWizardLocation")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
            self.driver.execute_script("arguments[0].click();", link)
        except NoSuchElementException:
            link = self.driver.find_element(
                By.XPATH, "//a[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add') and contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'service')]"
            )
            self.driver.execute_script("arguments[0].click();", link)

        # Wait for modal
        modal_el = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.ID, "myAddServiceLocationView"))
        )
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "AddServiceLocationBodyContainer"))
        )

        modal_css = "#myAddServiceLocationView"

        # Equipment Category if visible
        try:
            cat = self.driver.find_element(By.CSS_SELECTOR, f"{modal_css} #Svc_EquipmentCategoryID")
            if cat.is_displayed():
                Select(cat).select_by_visible_text("Recycler")
        except (NoSuchElementException, TimeoutException):
            pass

        # Select2 fields
        select2_select(self.driver, f"{modal_css} #select2-Svc_EquipmentTypeID-container", "Norbert Recycler")
        select2_select(self.driver, f"{modal_css} #select2-Svc_ServiceTypeID-container", "BULK SERVICE")
        select2_select(self.driver, f"{modal_css} #select2-Svc_FrequencyTypeID-container", "5 days per week")

        # Ownership
        try:
            own = self.driver.find_element(By.CSS_SELECTOR, f"{modal_css} #ddlSvc_OwnerShipID")
            Select(own).select_by_index(1)
        except (NoSuchElementException, TimeoutException):
            pass

        # Next x2
        self._click_add_service_next()
        self._click_add_service_next()

        # Routing step
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "divAddServiceRoutingContainer"))
        )
        for i in range(5):
            day_dd = self.driver.find_element(By.CSS_SELECTOR, f"{modal_css} #ddlDayofWeeek_{i}")
            Select(day_dd).select_by_value(str(i + 1))
            select2_select(self.driver, f"{modal_css} #select2-ddlDayofRoute_{i}-container", "Automation test 1")

        self._click_add_service_next()

        # Next step (charges)
        btn4 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'{modal_css} button[onclick*="ShowNextMyAddServiceLocationPopUp(4)"]'))
        )
        btn4.click()

        # Requested By
        req_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Svc_RequestedBy"))
        )
        req_field.clear()
        req_field.send_keys(requested_by or USER_DATA.get("automation_user", "AutoMVC"))

        # Change Reason & Service Code
        select2_select(self.driver, f"{modal_css} #select2-Svc_ServiceChangeReasonID-container", "NEW CUST")
        select2_select(self.driver, f"{modal_css} #select2-NewSvcCode_1-container", "DELFLAT")

        # Add charge
        add_charge = self.driver.find_element(By.CSS_SELECTOR, f"{modal_css} #addUpdateNewCharge_1")
        add_charge.click()

        # Route for service code workflow
        route_container = '[id^="select2-ddlDayRouteServiceCodeWorkflow_"][id$="-container"]'
        containers = self.driver.find_elements(By.CSS_SELECTOR, f"{modal_css} {route_container}")
        select2_select(self.driver, f"{modal_css} {route_container}", "Automation test 1")
        if len(containers) >= 2:
            # Select2 for second container
            select2_select(self.driver, f"{modal_css} {route_container}", "Automation test 1")

        # Submit
        submit_btn = self.driver.find_element(
            By.CSS_SELECTOR, f'{modal_css} button[onclick="ShowTemporaryServicePopup()"]'
        )
        submit_btn.click()
        _wfls(self.driver)

        # Verify success
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((
                By.XPATH, "//*[contains(text(),'Service has been created successfully')]"
            ))
        )

        # Wait for services list to refresh
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "services_list_container"))
        )
        # Click the last service
        self.select_last_service()

    def _click_add_service_next(self):
        """Click the visible Next button in the Add Service modal."""
        footers = self.driver.find_elements(
            By.CSS_SELECTOR, "#myAddServiceLocationView .myAddServiceBtnFooter"
        )
        for footer in footers:
            if footer.is_displayed():
                btns = footer.find_elements(By.XPATH, ".//button[contains(text(),'Next')]")
                for btn in btns:
                    if btn.is_displayed():
                        btn.click()
                        return

    def get_service_info_heading(self):
        """Return the first visible Service Info heading element."""
        headings = self._find_service_info_headings()
        for h in headings:
            if h.is_displayed():
                return h
        return headings[0] if headings else None

    def expand_service_info(self):
        """Expand the first Service Info block by clicking its heading."""
        heading = self.get_service_info_heading()
        if heading:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", heading)
            self.driver.execute_script("arguments[0].click();", heading)

    # ── Service Activity tab helpers ──────────────────────────────

    # Service Activity tab pane and calendar selectors
    SA_TAB_PANE = (By.ID, "parentTabContainer_3")
    SA_CALENDAR_CONTAINER = (By.ID, "serviceHistoryCalendarContainerDiv")
    SA_LIST_VIEW_CONTAINER = (By.ID, "serviceHistoryListViewContainerDiv")
    SA_MONTH_DISPLAY = (By.ID, "select2-months-container")
    SA_PREV_BTN = (By.CSS_SELECTOR, 'button.fc-prev-button[aria-label="prev"]')
    SA_NEXT_BTN = (By.CSS_SELECTOR, 'button.fc-next-button[aria-label="next"]')
    SA_SHOW_ALL_CHECKBOX = (By.ID, "ShowAllOrders")
    SA_SERVICE_DISPLAY_DROPDOWN = (By.CSS_SELECTOR, ".openServiceCalendarFilter")
    SA_SERVICE_DISPLAY_TEXT = (By.CSS_SELECTOR, ".multiServiceLocation span")
    SA_LIST_VIEW_ICON = (By.ID, "list-viewicon")
    SA_CALENDAR_VIEW_ICON = (By.ID, "calender-viewicon")
    SA_FILTER_ICON = (By.ID, "SnapshotServiceActivityFilter")
    SA_FILTER_DROPDOWN = (By.ID, "dispatchfilterContent")
    SA_FILTER_LOAD_BTN = (By.ID, "snapshotfilterBtn")
    SA_CALENDAR_EVENT = (By.CSS_SELECTOR, ".fc-day-grid-event")
    SA_CALENDAR_TOOLTIP_TRIGGER = (By.CSS_SELECTOR, "span.calendar-tool-tip-trigger")
    SA_CALENDAR_TOOLTIP_POPUP = (By.CSS_SELECTOR, "div.calendar-tool-tip-content.popover")

    # Calendar Choose Option modal
    SA_CALENDAR_OPTION_MODAL = (By.ID, "myCalendarOptionModalDialog")
    SA_SELECTED_DATE_SPAN = (By.ID, "spnSelectedDateFromCalender")
    SA_BTN_ADD_ORDER = (By.ID, "btnCreateNewOrder")
    SA_TXT_FILTER_SERVICE = (By.ID, "txtFilterServiceOpenTable")
    SA_NEW_ORDER_HEADER = (By.ID, "cTabActivityPopUpHeader")
    SA_NEW_ORDER_BODY = (By.ID, "cTabActivityPopUpBody")
    SA_ORDER_TYPE_CONTAINER = (By.ID, "select2-order_Type-container")
    SA_ORDER_ROUTE_CONTAINER = (By.ID, "select2-order_Route-container")
    SA_ORDER_REQUEST_BY = (By.ID, "order_RequestBy")
    SA_BTN_CREATE_ORDER = (By.ID, "btnCreateServiceOrder")
    SA_BTN_ADD_ACTIVITY_CALENDAR = (
        By.CSS_SELECTOR, 'button[onclick="AddNewServiceActivityNote(1)"]'
    )
    SA_ADD_ACTIVITY_MODAL = (By.ID, "myCTabAddEditNoteNewModal")
    SA_ADD_ACTIVITY_HEADER = (By.ID, "cTabActivityPopUpNewHeader")
    SA_TYPE_DROPDOWN = (By.ID, "select2-Svc_ATabDDlType-container")
    SA_CONTACT_INPUT = (By.ID, "Svc_ATabContact")
    SA_REMINDER_CHECKBOX = (By.ID, "Reminder")
    SA_REMINDER_TYPE_DROPDOWN = (By.ID, "select2-ddlType-container")
    SA_REMINDER_DESCRIPTION = (By.ID, "Description")
    SA_BTN_SAVE_ACTIVITY = (By.CSS_SELECTOR, 'input[onclick="AddTabNotesDetail()"]')
    SA_BTN_ADD_FILE_CALENDAR = (
        By.CSS_SELECTOR, 'button[onclick="AddNewServiceActivityNote(2)"]'
    )
    SA_ADD_FILE_HEADER = (By.ID, "cTabActivityPopUpNewHeader")
    SA_TRIGGER_FILE_INPUT = (By.ID, "triggerFileInput")
    SA_FILE_INPUT = (By.ID, "Svc_ATabNoteFile_1")
    SA_FILE_DESCRIPTION = (By.ID, "Svc_ATabFileDescription")
    SA_TGL_CUSTOMER_PORTAL_VISIBLE = (By.ID, "tglAddFileCustomerPortalVisible")
    SA_BTN_SAVE_FILE = (By.CSS_SELECTOR, 'input[onclick="AddFileTabNotesDetail()"]')

    # Suggest route / Nearby Services
    SA_BTN_SUGGEST = (
        By.CSS_SELECTOR,
        'a[onclick*="DisplayServiceRoutingPopup"][onclick*="SuggestRoute"]',
    )
    SA_NEARBY_SERVICES_MODAL = (By.ID, "commonHistoryMapPopupRouting")
    SA_NEARBY_SERVICES_TITLE = (By.ID, "myMapViewLabelRouting")
    SA_BTN_CLOSE_NEARBY = (
        By.CSS_SELECTOR,
        'button.closeBtn[onclick*="CloseServiceInfoPopUpRouting"]',
    )

    # Work order modal selectors
    WO_MODAL_WRAPPER = (By.ID, "myWorkOrderView123")
    WO_MODAL_CONTENT = (By.CSS_SELECTOR, "#myWorkOrderView123 .modal-content.common")
    WO_MODAL_HEADER = (By.ID, "divModalHeader")
    WO_MODAL_TITLE = (By.ID, "myWorkOrderLabel")
    WO_MODAL_BODY = (By.ID, "WorkOrderContainer")
    WO_MODAL_TOP_INFO = (By.CSS_SELECTOR, ".clsordertop-info")
    WO_MODAL_TABS_LIST = (By.ID, "woChildTabContainerOrder")
    WO_STATUS_SELECT = (By.CSS_SELECTOR, "#myWorkOrderView123 #ddlServiceHistoryStatus")
    WO_STATUS_SELECT2 = (
        By.CSS_SELECTOR,
        "#myWorkOrderView123 #select2-ddlServiceHistoryStatus-container",
    )
    WO_BTN_CLOSE = (
        By.CSS_SELECTOR,
        '#myWorkOrderView123 button.btn-secondary[onclick*="ReBindBillingAuditSummaryDetailDisplayBody"]',
    )

    # Work order modal child tab link selectors
    WO_TAB_INFORMATION = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_1"][onclick*="ContactOrderDetailAllTabActive(1)"]',
    )
    WO_TAB_ACCESS = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_2"][onclick*="ContactOrderDetailAllTabActive(2)"]',
    )
    WO_TAB_BILLING = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_3"][onclick*="ContactOrderDetailAllTabActive(3)"]',
    )
    WO_TAB_EQUIPMENT = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_4"][onclick*="ContactOrderDetailAllTabActive(4)"]',
    )
    WO_TAB_ATTACHMENTS = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_5"][onclick*="ContactOrderDetailAllTabActive(5)"]',
    )
    WO_TAB_STATUS_HISTORY = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_6"][onclick*="ContactOrderDetailAllTabActive(6)"]',
    )
    WO_TAB_AUDIT = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_7"][onclick*="ContactOrderDetailAllTabActive(7)"]',
    )
    WO_TAB_EVENTS = (
        By.CSS_SELECTOR,
        'a[href="#woChildTabContainerOrder_10"][onclick*="ContactOrderDetailAllTabActive(10)"]',
    )

    # Work order modal child tab pane selectors (IDs)
    WO_PANE_INFORMATION = (By.CSS_SELECTOR, "#woChildTabContainerOrder_1.tab-pane")
    WO_PANE_ACCESS = (By.CSS_SELECTOR, "#woChildTabContainerOrder_2.tab-pane")
    WO_PANE_BILLING = (By.CSS_SELECTOR, "#woChildTabContainerOrder_3.tab-pane")
    WO_PANE_EQUIPMENT = (By.CSS_SELECTOR, "#woChildTabContainerOrder_4.tab-pane")
    WO_PANE_ATTACHMENTS = (By.CSS_SELECTOR, "#woChildTabContainerOrder_5.tab-pane")
    WO_PANE_STATUS_HISTORY = (By.CSS_SELECTOR, "#woChildTabContainerOrder_6.tab-pane")
    WO_PANE_AUDIT = (By.CSS_SELECTOR, "#woChildTabContainerOrder_7.tab-pane")
    WO_PANE_EVENTS = (By.CSS_SELECTOR, "#woChildTabContainerOrder_10.tab-pane")

    # Send SMS selectors
    WO_SMS_OPEN_BTN = (
        By.CSS_SELECTOR,
        '#myWorkOrderView123 button[onclick*="ShowOrderDetailSMSPopup"]',
    )
    MODAL_ORDER_DETAIL_SMS = (By.ID, "modalOrderDetailSMS")
    DDL_ORDER_SMS_TEMPLATE = (By.ID, "ddlOrderDetailSMSTemplate")
    TXT_ORDER_SMS_CONTACT = (By.ID, "txtOrderDetailSMSContact")
    BTN_ORDER_SMS_SEND = (By.CSS_SELECTOR, ".btnOrderDetalEmailSMS")
    MODAL_CONTACT_SUGGESTIONS = (By.ID, "modalContactSuggestions")

    # Send Email / Print selectors
    WO_EMAIL_OPEN_BTN = (
        By.CSS_SELECTOR,
        '#myWorkOrderView123 button[onclick*="SendOperationsAlertEmailToUser"][onclick*=",2)"]',
    )
    WO_PRINT_OPEN_BTN = (
        By.CSS_SELECTOR,
        '#myWorkOrderView123 button[onclick*="SendOperationsAlertEmailToUser"][onclick*=",1)"]',
    )
    MODAL_SEND_OPS_EMAIL = (By.ID, "sendOpsAlertEmailPopUp")
    TXT_OPS_EMAIL_ADDRESS = (By.ID, "txtOpsEmailAddress")
    DDL_PRINT_ORDER_TEMPLATE = (By.ID, "ddlPrintOrderTemplate")
    CHK_INCLUDE_ORDER_PDF = (By.ID, "chkIncludeOrderPDF")
    CHK_INCLUDE_SELECTED_ATTACHMENTS = (By.ID, "chkIncludeSelectedAttachments")
    BTN_EMAIL_ORDER = (By.ID, "btnEmailOrder")
    BTN_PRINT_ORDER = (By.ID, "btnPrintOrder")

    # Information tab selectors
    WO_INFO_DESTINATION_EDIT = (
        By.CSS_SELECTOR, 'a[onclick*="openFormEneryDestination"]'
    )
    WO_DESTINATION_MODAL = (By.ID, "myAddServiceLocationView")
    WO_DESTINATION_SELECT = (By.ID, "ddlDestinationFromEntry")
    WO_DESTINATION_UPDATE_BTN = (
        By.CSS_SELECTOR,
        'input.btn-primary[value="Update"][onclick*="SaveFormEntryDestination"]',
    )
    WO_PRIORITY_SPAN = (By.ID, "spnOrderDetailServiceHistoryPriority")
    WO_PRIORITY_OPEN_LINK = (
        By.CSS_SELECTOR,
        'a[onclick*="showOrderDetailServiceHistoryPriorityModal"]',
    )
    WO_PRIORITY_SELECT = (By.ID, "ddlOrderDetailServiceHistoryPriority")
    WO_PRIORITY_UPDATE_BTN = (
        By.CSS_SELECTOR,
        'input.btn-primary[onclick*="updateOrderDetailServiceHistoryPriority"]',
    )
    WO_ORDER_NOTE_EDIT_LINK = (By.CSS_SELECTOR, 'a[onclick*="EditInfoNote"]')
    WO_ORDER_NOTE_TEXTAREA = (By.CSS_SELECTOR, 'textarea[id^="txtNoteResponseField_"]')
    WO_ORDER_NOTE_SAVE_BTN = (By.CSS_SELECTOR, 'button[onclick*="saveInfoNote"]')
    WO_ORDER_NOTE_ALERT_TOGGLE = (By.ID, "chkServcieNoteAlert")

    # Location Detail (Information tab)
    WO_LOCATION_DETAIL_MAP_LINK = (
        By.CSS_SELECTOR, 'a[onclick*="historyBothAddressInMapView"]'
    )
    WO_SCHEDULED_LOCATION_TITLE = (By.ID, "myDifferentMapViewLabel")
    WO_SCHEDULED_LOCATION_MAP = (By.ID, "DifferentMpCanvasView")

    # Operations Results (Information tab)
    WO_OPS_SEQUENCE_LINK = (By.CSS_SELECTOR, 'div[id^="spnDispatchLinkSequenceOrder_"] a')
    WO_OPS_ROUTE_CONTAINER = (By.CSS_SELECTOR, 'div[id^="spnDispatchLinkRouteOrder_"]')
    WO_OPS_ROUTE_REASSIGN_LINK = (
        By.CSS_SELECTOR,
        'div[id^="spnDispatchLinkRouteOrder_"] a[onclick*="GoToRoutePopUpOrderDetial"]',
    )
    WO_REASSIGN_ROUTE_MODAL = (By.ID, "MainRouteContainerOrder")
    WO_OPS_ETA_WIDGET = (
        By.CSS_SELECTOR, 'div[id^="divDispatchLinkEstimatedArrivalTimeOrder_"]'
    )
    WO_SEQUENCE_MODAL_HEADING = (By.ID, "hOrderSequenceUpdate")
    WO_SEQUENCE_ROUTE_INPUT = (By.ID, "txtRouteSequence")
    WO_SEQUENCE_ETA_INPUT = (By.ID, "txtEstimatedArrivalTime")
    WO_SEQUENCE_UPDATE_BTN = (
        By.CSS_SELECTOR,
        'input.btn-primary.modalBtn[value="Update"][onclick*="SaveRouteSequence"]',
    )
    WO_OPS_RESPONSE_EDIT_LINK = (
        By.CSS_SELECTOR,
        '.operationResponseDiv a[onclick*="EditInfoResponseField"]',
    )
    WO_OPS_RESPONSE_TEXTAREA = (
        By.CSS_SELECTOR, 'textarea[id^="txtInfoResponseField_"]'
    )
    WO_OPS_RESPONSE_SAVE_BTN = (
        By.CSS_SELECTOR, 'button.savebtn[onclick*="saveInfoResponseField"]'
    )
    WO_OPS_RESPONSE_DISPLAY = (By.CSS_SELECTOR, 'span[id^="spnInfoResponseField_"]')
    WO_PERFORMED_LOCATION_MAP_LINK = (
        By.CSS_SELECTOR,
        '.performed-location a[onclick*="historyBothAddressInMapView"]',
    )

    # Access tab selectors
    WO_ACCESS_START_TIME = (By.ID, "AccessStartTime")
    WO_ACCESS_END_TIME = (By.ID, "AccessEndTime")

    # Equipment tab selectors
    WO_EQUIP_DELIVER_SERIAL = (By.ID, "TabequipMoveDSN")
    WO_EQUIP_SERIAL_SEARCH = (
        By.CSS_SELECTOR,
        '#woChildTabContainerOrder_4 .search-serial-number[onclick*="getAllInventoryList"]',
    )
    WO_EQUIP_SAVE_BTN = (By.ID, "btnSaveTabEquipmentMove")
    WO_EQUIP_HISTORY_CONTAINER = (By.ID, "divEquipmentHistoryContainer")
    WO_EQUIP_HISTORY_TABLE = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_4 #divEquipmentHistoryContainer table.table.table-bordered",
    )
    WO_SERIAL_SEARCH_MODAL = (By.CSS_SELECTOR, "#CommonLayoutPopUpContainer.modal-content.common")
    WO_SERIAL_SEARCH_YARD_FILTER = (By.ID, "ddlEquipmentYard")
    WO_SERIAL_SEARCH_GRID = (By.ID, "tableEquipmentHistoryYard")

    # Attachments tab selectors
    WO_SIGNATURE_REQUIRED = (By.ID, "SignatureRequired")
    WO_IMAGE_REQUIRED = (
        By.CSS_SELECTOR,
        '#woChildTabContainerOrder_5 input.ddlCommonSig_AttRequired.hiddenSwitch-Checkbox[name="ImageRequired"]',
    )
    WO_ADD_ORDER_ATTACHMENT_FILE = (By.ID, "AddOrderAttachmentFile")
    WO_ATTACHMENT_ADD_FILE_WRAP = (By.CSS_SELECTOR, ".attachmentFile-OuterWrap")

    # Events tab selectors
    WO_EVENTS_TABLE = (By.ID, "EventLogServiceHistoryTable")
    WO_EVENTS_TABLE_BODY = (By.CSS_SELECTOR, "tbody.tBodyEventLogServiceHistory")

    # Status History tab selectors
    WO_STATUS_HISTORY_TABLE = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_6 table.table.table-bordered.dataTable",
    )

    # Billing tab selectors
    WO_BILLING_PO_EDIT = (By.ID, "btnEditPo")
    WO_BILLING_PO_COPY = (By.ID, "txtShowPoNumberCopy")
    WO_BILLING_PO_SAVE = (By.ID, "btnSavePo")
    WO_BILLING_PAYMENT_REQUIRED = (By.ID, "textPaymentRequired")
    WO_BILLING_STATUS_SELECT = (By.ID, "ddlBillingStatusBillingTab")
    WO_BILLING_BTN_RECALCULATE = (By.ID, "btnReCalculate")
    WO_BILLING_BTN_ADD_CHARGE = (By.ID, "btnShowAddNewChargeRow")
    WO_BILLING_ADD_CHARGE_ROW = (By.ID, "allchargeinputfield")
    WO_BILLING_NEW_CHARGE_SVC = (By.ID, "ddlServiceCode")
    WO_BILLING_CHARGES_TABLE = (By.ID, "tblBilling")
    WO_BILLING_CHARGES_WRAP = (By.ID, "divServiceHistoryChargeBody")
    WO_DISPOSAL_SECTION = (By.ID, "divRouteTripDisposalContainer")
    WO_DISPOSAL_ADD_LINK = (By.CSS_SELECTOR, 'a[onclick*="ShowAddNewDisposalRow"]')
    WO_DISPOSAL_TABLE = (
        By.CSS_SELECTOR, "#divRouteTripDisposalContainer table.manage_drivehelper"
    )
    WO_DISPOSAL_AUDIT_MODAL = (By.ID, "RouteTripDisposalAuditPopUp")
    WO_DISPOSAL_AUDIT_TITLE = (By.ID, "TitleRouteTripDisposalAudit")

    # Success message
    SUCCESS_MSG = (By.ID, "divSucessContent")

    def ensure_service_activity_calendar_ready(self):
        """Assert the calendar container is visible inside the Service Activity tab."""
        self.find_visible(*self.SA_TAB_PANE, timeout=15)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SA_CALENDAR_CONTAINER)
        )

    def get_current_date_iso(self):
        """Return current local date as YYYY-MM-DD (matches FullCalendar data-date)."""
        from datetime import date
        return date.today().isoformat()

    def get_date_display_from_iso(self, iso_date):
        """Convert YYYY-MM-DD to MM/DD/YYYY."""
        parts = iso_date.split("-")
        return f"{parts[1]}/{parts[2]}/{parts[0]}"

    def open_calendar_option_modal(self, date_iso=None):
        """Click today's calendar cell to open the Choose Option modal."""
        if date_iso is None:
            date_iso = self.get_current_date_iso()
        display = self.get_date_display_from_iso(date_iso)
        self.ensure_service_activity_calendar_ready()
        self.wait_for_loading_screen()
        cell_selector = f'td.fc-day[data-date="{date_iso}"]'
        cell = self.find_visible(By.CSS_SELECTOR, cell_selector, timeout=10)
        self.driver.execute_script("arguments[0].click();", cell)
        self.find_visible(*self.SA_CALENDAR_OPTION_MODAL, timeout=60)
        span = self.find_visible(*self.SA_SELECTED_DATE_SPAN, timeout=10)
        assert span.text == display
        self.wait_for_loading_screen()

    def open_work_order_from_calendar_today(self):
        """Click today's calendar event to open the work order modal."""
        self.ensure_service_activity_calendar_ready()
        date_iso = self.get_current_date_iso()
        js = """
        var container = document.getElementById('serviceHistoryCalendarContainerDiv');
        var todayCell = container.querySelector('td.fc-day.fc-today') ||
                        container.querySelector('td.fc-day[data-date="' + arguments[0] + '"]');
        if (!todayCell) return false;
        var events = container.querySelectorAll('[id^="svcHisCalendarDiv_"], .fc-day-grid-event, a.fc-event, .fc-event');
        var cellRect = todayCell.getBoundingClientRect();
        for (var i = 0; i < events.length; i++) {
            var r = events[i].getBoundingClientRect();
            if (r.width <= 0 || r.height <= 0) continue;
            var cx = (r.left + r.right) / 2;
            var cy = (r.top + r.bottom) / 2;
            if (cx >= cellRect.left && cx <= cellRect.right && cy >= cellRect.top && cy <= cellRect.bottom) {
                events[i].click();
                return true;
            }
        }
        for (var j = 0; j < events.length; j++) {
            var r2 = events[j].getBoundingClientRect();
            if (r2.width > 0 && r2.height > 0) {
                events[j].click();
                return true;
            }
        }
        return false;
        """
        result = self.driver.execute_script(js, date_iso)
        assert result, "No calendar event found to click for today"
        self.wait_for_loading_screen()

    def activate_work_order_child_tab(self, tab_link_locator, tab_pane_locator):
        """Click a work order modal child tab and wait for it to become active."""
        self.find_visible(*self.WO_MODAL_WRAPPER, timeout=20)
        tab_link = self.find_visible(*tab_link_locator, timeout=15)
        tab_link.click()
        self.wait_for_loading_screen()
        WebDriverWait(self.driver, 10).until(
            lambda d: "active" in self.find_element(*tab_pane_locator).get_attribute("class")
        )

    def open_work_order_modal_tab(self, tab_link_locator, tab_pane_locator):
        """Open today's work order, then activate a child tab."""
        self.open_work_order_from_calendar_today()
        self.activate_work_order_child_tab(tab_link_locator, tab_pane_locator)

    def assert_record_updated_success(self, timeout=20):
        """Assert the success banner is visible with 'Record has been ... successfully'."""
        import re
        pattern = re.compile(
            r"Record has been (updated|added|addded|deleted) successfully", re.IGNORECASE
        )
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            lambda d: any(
                pattern.search(el.text)
                for el in d.find_elements(
                    By.CSS_SELECTOR,
                    "#displayMsg, #msgBillAlert, #divSucessContent, #divSucessContentHistory"
                )
                if el.text.strip()
            )
        )

    def select2_click_option(self, container_css, option_text, timeout=8):
        """Open a Select2 dropdown and click an option by text."""
        container = self.find_clickable(By.CSS_SELECTOR, container_css, timeout=timeout)
        container.click()
        option = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f'//li[contains(@class,"select2-results__option") and contains(text(),"{option_text}")]'
            ))
        )
        option.click()

    def scroll_disposal_table_right(self):
        """Scroll disposal table .table-responsive wrappers fully right."""
        self.driver.execute_script("""
            var section = document.getElementById('divRouteTripDisposalContainer');
            if (section) {
                var wraps = section.querySelectorAll('.table-responsive');
                wraps.forEach(function(w) { w.scrollLeft = w.scrollWidth; });
            }
        """)

    def run_native_onclick(self, onclick_str):
        """Execute an onclick attribute string in the app window context."""
        self.driver.execute_script(onclick_str)
