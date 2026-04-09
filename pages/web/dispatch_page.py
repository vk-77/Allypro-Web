"""
Dispatch page object for the Dispatch Map and Dispatch Board.

Provides helpers for map/board navigation, route filtering, work-order
tab interaction, drag-and-drop, notes, and schedule management.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from .base_web_page import BasePage


class DispatchPage(BasePage):
    """Page object for Dispatch Map and Dispatch Board pages."""

    # ── Navigation locators ────────────────────────────────────────
    PAGE_TITLE = (By.CSS_SELECTOR, "#content p.pageTitle")

    DISPATCH_MAP_LINK = (By.CSS_SELECTOR, '[href="/DispatchDashboard"]')
    DISPATCH_BOARD_LINK = (
        By.CSS_SELECTOR, '[href="/DispatchDashboard/DispatchBoard"]'
    )

    MAP_CANVAS = (By.ID, "map-canvas")
    DISPATCH_BOARD = (By.CSS_SELECTOR, "#dispatchBoard, .dispatch-board")
    ROUTE_SELECT = (By.ID, "ddlRoute")

    SUCCESS_MESSAGE = (By.ID, "divSucessContent")

    # ── Dispatch Map locators ──────────────────────────────────────
    LOAD_DISPATCH_GRID_BTN = (
        By.CSS_SELECTOR, '[onclick="LoadDispatchGrid()"]'
    )
    LEFT_PANEL_ACCORDION = (By.ID, "leftPanelAccordionContainer")
    PANEL_DEFAULT = (By.CSS_SELECTOR, ".panel.panel-default")
    EXPAND_ICON_101 = (By.ID, "expandicon_101")
    EXPAND_ICON_102 = (By.ID, "expandicon_102")
    ROUTE_BOX_BTN = (By.CSS_SELECTOR, "#routeBoxBtn i.fa")
    ROUTE_BOX_PANEL_SELECT_REGION = (
        By.CSS_SELECTOR, "#routeBoxPanel span.select-region"
    )
    RIGHT_PANEL_ROUTE_FILTER_FIRST = (
        By.CSS_SELECTOR,
        "#setrightpanelroutefilter li:nth-child(1) label.checkbox",
    )
    REGION_FILTER_ARROW = (
        By.CSS_SELECTOR, "#content li.clsRegionFilterDiv a.select-arrow"
    )
    MAP_SEARCH_BTN = (By.CSS_SELECTOR, "#content li:nth-child(12) a.btn")
    WA_CHECKBOX = (By.CSS_SELECTOR, '#content input[value="WA"]')

    # ── Dispatch Board locators ────────────────────────────────────
    BOARD_SEARCH_BTN = (By.CSS_SELECTOR, "#content li:nth-child(13) a.btn")
    ROUTE_FILTER_ARROW = (
        By.CSS_SELECTOR, "#content li.clsRouteFilter a.select-arrow"
    )
    DISPATCH_BOARD_ROUTE_LIST = (
        By.CSS_SELECTOR, "#content ul.dispatch-board-route"
    )
    FLEX_WRAP_LIST = (By.CSS_SELECTOR, "#content ul.flex-wrap")

    # Work order tabs
    WO_TAB_ORDER_1 = (By.CSS_SELECTOR, "#woChildLiTabOrder_1 a.nav-link")
    WO_TAB_ORDER_2 = (By.CSS_SELECTOR, "#woChildLiTabOrder_2 a.nav-link")
    WO_TAB_ORDER_3 = (By.CSS_SELECTOR, "#woChildLiTabOrder_3 a.nav-link")
    WO_TAB_ORDER_5 = (By.CSS_SELECTOR, "#woChildLiTabOrder_5 a.nav-link")
    WO_TAB_ORDER_6 = (By.CSS_SELECTOR, "#woChildLiTabOrder_6 a.nav-link")
    WO_TAB_ORDER_7 = (By.CSS_SELECTOR, "#woChildLiTabOrder_7 a.nav-link")
    WO_TAB_ORDER_10 = (By.CSS_SELECTOR, "#woChildLiTabOrder_10 a.nav-link")

    # Work order tab 1 content
    WO_TAB1_LOCATION = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.location div.text-center",
    )
    WO_TAB1_SERVICED = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.serviced div.text-center",
    )
    WO_TAB1_RECENTLY_VIEWED = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.recently-viewed div.text-center",
    )
    WO_TAB1_ADD_NOTE_BTN = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 li:nth-child(1) > a.btn > svg.svg_fill",
    )
    WO_TAB1_LOCATION_TEXTAREA = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.location textarea.form-control",
    )
    WO_TAB1_LOCATION_SAVE_SVG = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.location svg.svg_stroke",
    )
    WO_TAB1_OPERATION_NOTE_BTN = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.operationResponseDiv svg.svg_fill",
    )
    WO_TAB1_OPERATION_TEXTAREA = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.operationResponseDiv textarea.form-control",
    )
    WO_TAB1_OPERATION_SAVE_BTN = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_1 div.operationResponseDiv button.savebtn",
    )

    # Work order tab 2 content
    WO_TAB2_PANEL_CENTER = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_2 div:nth-child(1) > div.panel > div.text-center",
    )
    WO_TAB2_LOCATION = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_2 div.location div.text-center",
    )

    # Work order tab 3 content
    ADD_NEW_CHARGE_BTN = (By.ID, "btnShowAddNewChargeRow")
    ROUTE_TRIP_DISPOSAL_CONTAINER = (By.ID, "divRouteTripDisposalContainer")
    ROUTE_TRIP_DISPOSAL_BTN = (
        By.CSS_SELECTOR, "#divRouteTripDisposalContainer a.btn"
    )

    # Work order tab 5 content
    ADD_ORDER_ATTACHMENT_FILE = (By.ID, "AddOrderAttachmentFile")
    WO_TAB5_SIGNATURE_TEXT = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_5 div:nth-child(1) > div:nth-child(2) "
        "> div.panel > div.row > div.signature-text > strong",
    )
    WO_TAB5_NOTES_TEXT = (
        By.CSS_SELECTOR,
        "#woChildTabContainerOrder_5 div:nth-child(2) > div.panel "
        "> div.add-file > div.form-group > span",
    )

    # Filters
    HIDE_REGION_SPAN = (By.CSS_SELECTOR, "#content span.hideRegion")
    BUSINESS_UNIT_FILTER_ARROW = (
        By.CSS_SELECTOR,
        "#content li.clsBuisnessUnitFilter a.select-arrow",
    )
    BU_SEGMENT_2ND = (
        By.CSS_SELECTOR,
        "#content div.mutliSelectSegment li:nth-child(2) label.checkbox",
    )
    DEFAULT_BU_CHECKBOX = (
        By.CSS_SELECTOR,
        '#content input[data-name="Default Business Unit"]',
    )
    BU_SEGMENT_3RD = (
        By.CSS_SELECTOR,
        "#content div.mutliSelectSegment li:nth-child(3) label.checkbox",
    )
    TEST_DATA_CHECKBOX = (
        By.CSS_SELECTOR, '#content input[data-name="Test data "]'
    )
    ROUTE_FILTER_SELECT_ALL = (
        By.CSS_SELECTOR, '#content a[data-open="1"]'
    )
    YARD_FILTER_ARROW = (
        By.CSS_SELECTOR, "#content li.clsYardFilter a.select-arrow"
    )
    EQUIPMENT_TYPE_FILTER_ARROW = (
        By.CSS_SELECTOR,
        "#content li.clsEquipmentTypeFilter a.select-arrow",
    )
    EQUIPMENT_TYPE_2ND = (
        By.CSS_SELECTOR,
        "#content div.mutliSelectEquipmentType li:nth-child(2) label.checkbox",
    )
    EQUIPMENT_20YDRO = (
        By.CSS_SELECTOR, '#content input[value="20YDRO"]'
    )
    SUPERVISOR_FILTER_ARROW = (
        By.CSS_SELECTOR,
        "#content li.clsSupervisorFilter a.select-arrow",
    )
    ORDER_TYPE_FILTER_ARROW = (
        By.CSS_SELECTOR,
        "#content li.clsOrderTypeFilter a.select-arrow",
    )
    ORDER_TYPE_2ND = (
        By.CSS_SELECTOR,
        "#content div.mutliSelectOrderType li:nth-child(2) label.checkbox",
    )
    END_SERVICE_CHECKBOX = (
        By.CSS_SELECTOR, '#content input[data-name="End service"]'
    )
    FILTER_LABEL_SVG = (
        By.CSS_SELECTOR, "#FilterLabel svg.svg_stroke"
    )
    SHOW_ALL_ORDERS = (By.CSS_SELECTOR, '[name="ShowAllOrders"]')
    MULTI_SEL_REGION = (
        By.CSS_SELECTOR, "#content p.multiSelRegion"
    )
    REGION_LABEL_14TH = (
        By.CSS_SELECTOR,
        "#content li:nth-child(2) li:nth-child(14) label.checkbox",
    )
    MULTI_SEL_EQUIPMENT = (
        By.CSS_SELECTOR, "#content p.multiSelEquipmentType"
    )

    # Print
    PRINT_ROUTE_LOG_TEMPLATE = (By.ID, "ddlPrintRouteLogTemplate")
    MODAL_ROUTE_LOG_PRINT_BTN = (
        By.CSS_SELECTOR, "#modalRouteLogPrint button.modalBtn"
    )

    # Map pin
    MAP_ICON_101 = (
        By.CSS_SELECTOR,
        "div.collapse_filter_box #mapIcon_101 img.three-eye",
    )
    BOARD_MAP_DIV = (
        By.CSS_SELECTOR,
        "#MapViewDiv div.gm-style > div:nth-child(1) > div:nth-child(2)",
    )

    # Apply permanent schedule
    APPLY_SEQ_ICON_101 = (By.CSS_SELECTOR, "#applySeqIcon_101 svg")
    SCHEDULE_UPDATE_MODAL = (By.ID, "modalServiceScheduleUpdateRouteLog")
    SCHEDULE_UPDATE_MODAL_CONTENT = (
        By.CSS_SELECTOR,
        "#modalServiceScheduleUpdateRouteLog div.col-xs-12",
    )
    SCHEDULE_UPDATE_MODAL_TITLE = (
        By.CSS_SELECTOR,
        "#modalServiceScheduleUpdateRouteLog h4.modal-title",
    )
    PROCESS_UPDATES_BTN = (By.ID, "btnProcessUpdateServiceScheduleUpdateRouteLog")
    EXPORT_LOG_BTN = (By.ID, "btnExportExcelServiceScheduleUpdateRouteLog")

    # Assigned orders
    ASSIGNED_SERVICES_TITLE = (
        By.CSS_SELECTOR,
        "#content div.row.pageTopHeader-Outer h4.modal-title",
    )

    # ── Navigation ─────────────────────────────────────────────────

    def navigate_to_dispatch_map(self):
        """Click the Dispatch Dashboard link and wait for load."""
        self.click_element(*self.DISPATCH_MAP_LINK)
        self.wait_for_loading_screen()

    def navigate_to_dispatch_board(self):
        """Click the Dispatch Board link and wait for load."""
        self.click_element(*self.DISPATCH_BOARD_LINK)
        self.wait_for_loading_screen()

    def get_page_title(self):
        """Return page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def is_map_visible(self):
        """Return True if map canvas is visible."""
        return self.element_is_visible(*self.MAP_CANVAS)

    # ── Dispatch Map actions ───────────────────────────────────────

    def click_load_dispatch_grid(self):
        """Click the Load Dispatch Grid button."""
        self.click_element(*self.LOAD_DISPATCH_GRID_BTN)
        self.wait_for_loading_screen()

    def expand_route_panel(self, panel_index, expand_icon_id):
        """Expand a route panel by index in the left accordion."""
        accordion = self.find_element(*self.LEFT_PANEL_ACCORDION)
        panels = accordion.find_elements(*self.PANEL_DEFAULT)
        icon = panels[panel_index].find_element(By.ID, expand_icon_id)
        self.driver.execute_script("arguments[0].click();", icon)

    def drag_order_between_routes(self, data_counter_value):
        """Drag an order from one route to another using data-counter."""
        selector = f'[data-counter="{data_counter_value}"]'
        sources = self.find_elements(By.CSS_SELECTOR, selector)
        if len(sources) < 2:
            raise ValueError(
                f"Expected at least 2 elements with data-counter="
                f"'{data_counter_value}', found {len(sources)}"
            )
        source = sources[0]
        target = sources[1]
        actions = ActionChains(self.driver)
        actions.click_and_hold(source).move_to_element(target).release().perform()

    # ── Dispatch Board actions ─────────────────────────────────────

    def click_board_search(self):
        """Click the search/apply button on the dispatch board."""
        self.click_element(*self.BOARD_SEARCH_BTN)

    def click_map_search(self):
        """Click the search/apply button on the dispatch map."""
        self.click_element(*self.MAP_SEARCH_BTN)

    def open_route_filter(self):
        """Open the route filter dropdown."""
        self.click_element(*self.ROUTE_FILTER_ARROW)

    def select_route_by_name(self, route_name):
        """Check a route checkbox by route name in the dispatch board list."""
        xpath = (
            f"//ul[contains(@class,'dispatch-board-route')]"
            f"//li[contains(.,'{route_name}')]"
            f"//input[contains(@class,'chkDispatchRoute')]"
        )
        checkbox = self.find_clickable(By.XPATH, xpath)
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_route_by_name(self, route_name):
        """Uncheck a route checkbox by route name."""
        xpath = (
            f"//ul[contains(@class,'dispatch-board-route')]"
            f"//li[contains(.,'{route_name}')]"
            f"//input[contains(@class,'chkDispatchRoute')]"
        )
        checkbox = self.find_clickable(By.XPATH, xpath)
        if checkbox.is_selected():
            checkbox.click()

    def close_route_filter(self):
        """Close the route filter by clicking the flex-wrap area."""
        self.click_element(*self.FLEX_WRAP_LIST)

    def click_first_work_order(self):
        """Click the first work order link."""
        self.click_element(
            By.CSS_SELECTOR, '[onclick^="ShowWorkOrder"]'
        )
        self.wait_for_loading_screen()

    def click_work_order_tab(self, tab_number):
        """Click a work order tab by number (1-10)."""
        tab_map = {
            1: self.WO_TAB_ORDER_1,
            2: self.WO_TAB_ORDER_2,
            3: self.WO_TAB_ORDER_3,
            5: self.WO_TAB_ORDER_5,
            6: self.WO_TAB_ORDER_6,
            7: self.WO_TAB_ORDER_7,
            10: self.WO_TAB_ORDER_10,
        }
        self.click_element(*tab_map[tab_number])
        self.wait_for_loading_screen()

    def add_location_note(self, text):
        """Add a location note on work order tab 1."""
        self.click_element(*self.WO_TAB1_ADD_NOTE_BTN)
        self.click_element(*self.WO_TAB1_LOCATION_TEXTAREA)
        self.type_text(*self.WO_TAB1_LOCATION_TEXTAREA, text)
        self.click_element(*self.WO_TAB1_LOCATION_SAVE_SVG)

    def add_operation_note(self, text):
        """Add an operation note on work order tab 1."""
        self.click_element(*self.WO_TAB1_OPERATION_NOTE_BTN)
        self.click_element(*self.WO_TAB1_OPERATION_TEXTAREA)
        self.type_text(*self.WO_TAB1_OPERATION_TEXTAREA, text)
        self.click_element(*self.WO_TAB1_OPERATION_SAVE_BTN)

    def select_print_template(self, template_value):
        """Select a print route log template by value."""
        el = self.find_element(*self.PRINT_ROUTE_LOG_TEMPLATE)
        Select(el).select_by_value(template_value)

    def click_print_modal_btn(self):
        """Click the print button in the route log print modal."""
        self.click_element(*self.MODAL_ROUTE_LOG_PRINT_BTN)
        self.wait_for_loading_screen()

    def click_apply_sequence_icon(self):
        """Click the apply permanent schedule icon for route 101."""
        self.click_element(*self.APPLY_SEQ_ICON_101)

    def click_process_updates(self):
        """Click the PROCESS UPDATES button."""
        self.click_element(*self.PROCESS_UPDATES_BTN)

    def click_export_log(self):
        """Click the EXPORT LOG button."""
        self.click_element(*self.EXPORT_LOG_BTN)
        self.wait_for_loading_screen()

    def open_new_tab(self):
        """Open a new tab and switch to it."""
        self.driver.execute_script("window.open('about:blank','_blank');")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        self.driver.get(self.driver.current_url)

    def is_disposal_container_visible(self, timeout=3):
        """Check if disposal container is visible."""
        return self.element_is_visible(
            *self.ROUTE_TRIP_DISPOSAL_CONTAINER, timeout=timeout
        )
