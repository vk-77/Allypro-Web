"""
Page object for the Elements Inventory pages.
"""
from selenium.webdriver.common.by import By

from .base_web_page import BaseWebPage


class InventoryPage(BaseWebPage):
    """
    Page object for Inventory Search page.
    """

    # ── Locators ──────────────────────────────────────────────────

    PAGE_TITLE = (By.CSS_SELECTOR, ".pageTitle")
    INVENTORY_MENU = (By.ID, "Active_1001")

    SEARCH_BTN = (By.CSS_SELECTOR, "#Inventory button.search_btn")
    ADD_INVENTORY_BTN = (By.CSS_SELECTOR, "#Inventory button.add_inventry_btn")
    INVENTORY_TABLE = (By.ID, "EquipmentInventoryTable")
    INVENTORY_ROWS = (By.CSS_SELECTOR, "#EquipmentInventoryTable tr")

    # Add inventory modal
    SERIAL_NUMBER = (By.ID, "txtAddSerialNbr")
    TAG_NUMBER = (By.ID, "txtAddTagNumber")
    YARD_SELECT = (By.CSS_SELECTOR, '[name="YardID"]')
    EQUIPMENT_TYPE_SELECT = (By.ID, "ddlAddEquipmentType")
    SAVE_CLOSE_BTN = (By.CSS_SELECTOR, '#btnSave\\\\&Close, [id="btnSave&Close"]')

    # Equipment move
    MOVE_TYPE_SELECT = (By.ID, "Manual_MoveType")
    MANUAL_YARD_SELECT = (By.CSS_SELECTOR, '[name="Manual_Yard"]')
    EQUIPMENT_STATUS_SELECT = (By.ID, "ddlEquipmentStatus")
    DETAIL_FIELD = (By.ID, "Detail")
    SAVE_MANUAL_BTN = (By.ID, "btnManualEquipmentSave")

    # Search filters
    SERIAL_SEARCH = (By.ID, "txtSerialNbr")

    # Inventory popup / details
    INVENTORY_POPUP_HEADER = (By.CSS_SELECTOR, "#InventoryPopup_1 div:nth-child(1) > div:nth-child(1) > h2")
    DETAILS_TAB = (By.CSS_SELECTOR, "#woInventoryChildLiTab_3 span")
    MOVE_HISTORY_TAB = (By.CSS_SELECTOR, "#woInventoryChildLiTab_2 a.nav-link")
    EDIT_EQUIP_BTN = (By.CSS_SELECTOR, "#inverntoryBodyContent button.edit_equip_btn")
    UPDATE_EQUIP_TYPE_BTN = (By.ID, "btnUpdateEquipmentType")
    MOVE_HISTORY_TABLE = (By.ID, "EquipmentMoveHistoryTable")

    # Add inventory modal tabs
    TAB_GENERAL = (By.CSS_SELECTOR, "#woChildLiTab_1 a.nav-link")
    TAB_REGISTRATION = (By.CSS_SELECTOR, "#woChildLiTab_2 a.nav-link")
    REGISTRATION_LABEL = (By.CSS_SELECTOR, "#RegistationTracking div:nth-child(3) > div.form-group > label.form-label")
    MODAL_GROUPING = (By.CSS_SELECTOR, "#modalAddInventory div.grouping")

    SUCCESS_MESSAGE = (By.ID, "divSucessContent")

    # ── Actions ───────────────────────────────────────────────────

    def open_inventory(self):
        """Click Inventory submenu."""
        self.click_element(*self.INVENTORY_MENU)
        self.wait_for_loading_screen()

    def click_search(self):
        """Click the Search button."""
        self.click_element(*self.SEARCH_BTN)
        self.wait_for_loading_screen()

    def click_add_inventory(self):
        """Click the Add Inventory button."""
        self.click_element(*self.ADD_INVENTORY_BTN)

    def get_page_title(self):
        """Return page title text."""
        return self.get_text(*self.PAGE_TITLE)

    def is_success_visible(self):
        """Return True if success message is visible."""
        return self.element_is_visible(*self.SUCCESS_MESSAGE)

    def get_success_message(self):
        """Return success message text."""
        return self.get_text(*self.SUCCESS_MESSAGE)
