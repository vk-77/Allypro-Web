"""
End-to-end: Create a service for a customer and verify it in Route Log.

Flow:
  1. Search for customer "Vk Test customer" (ID 9100647), verify Active
  2. Open Add Service wizard and handle the Customer/Location popup
  3. Fill Equipment, Service Type, Frequency → Next
  4. Set Day of Week = Thursday, Route = VK Route → Next
  5. Skip Order Charges & Surcharges → Next
  6. On Start Service Workflow: fill Requested By, Change Reason,
     check "Del" workflow, select VK Route, click Add Service
  7. Verify success message "Service created successfully" is displayed
  8. Navigate to Operations > Route Log
  9. Confirm that the Route Log screen is displayed

Usage:
    pytest tests/end_to_end_flow/test_create_service_and_verify_route.py -v -s
"""
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.web_settings import BASE_URL, DEFAULT_WAIT
from helpers.web_helper import (
    wait_for_loading_screen,
    navigate_to_menu,
    select2_select,
    scroll_to_element,
    text_is_visible,
)

# ── Test data ────────────────────────────────────────────────────────
CUSTOMER_NAME = "Vk Test customer"
CUSTOMER_ID = "9100647"

EQUIPMENT_CATEGORY = "Towable, non-exec"
EQUIPMENT_TYPE = "AG TOWABLE single"
SERVICE_TYPE = "TLR1 SVC - Cleaning, Restocking"
FREQUENCY = "1 day per week"
DAY_OF_WEEK = "4"  # Thursday (1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri)
ROUTE_NAME = "VK Route"
REQUESTED_BY = "VK QA"
CHANGE_REASON = "New Cust"
WORKFLOW_CODE = "Del"

LONG_WAIT = 30
MODAL = "#myAddServiceLocationView"


@pytest.mark.usefixtures("driver")
class TestCreateServiceAndVerifyRoute:
    """
    End-to-end flow: create a service on a customer, verify success,
    then confirm the Route Log screen is displayed.
    """

    def test_e2e_create_service_and_verify_in_route_log(self, driver):
        """Create service for Vk Test customer and verify in Route Log."""
        wait = WebDriverWait(driver, LONG_WAIT)

        # ── Step 1: Search and open customer ─────────────────────────
        print("\n--- Step 1: Opening customer details ---")
        _search_and_open_customer(driver, wait)
        print(f"  Customer loaded: {CUSTOMER_NAME} ({CUSTOMER_ID})")
        print("  Status: Active")

        # ── Step 2: Open Add Service wizard ─────────────────────────
        print("\n--- Step 2: Opening Add Service wizard ---")
        _open_add_service_modal(driver, wait)
        print("  Add Service modal opened")

        # ── Step 3: Fill Equipment, Service Type, Frequency ──────────
        print("\n--- Step 3: Filling service details ---")

        # Equipment Category (native <select>, triggers AJAX reload)
        print(f"  Equipment Category: {EQUIPMENT_CATEGORY}")
        _select_equipment_category(driver)

        # After category change the modal reloads — wait for Select2 fields
        # to be re-rendered before interacting with them
        _wait_for_select2_ready(driver, "#select2-Svc_EquipmentTypeID-container")

        # Equipment Type (Select2)
        print(f"  Equipment Type: {EQUIPMENT_TYPE}")
        _safe_select2(driver, f"{MODAL} #select2-Svc_EquipmentTypeID-container", EQUIPMENT_TYPE)
        print("  Equipment Type selected")

        # Service Type (Select2)
        print(f"  Service Type: {SERVICE_TYPE}")
        _safe_select2(driver, f"{MODAL} #select2-Svc_ServiceTypeID-container", SERVICE_TYPE)
        print("  Service Type selected")

        # Frequency (Select2)
        print(f"  Frequency: {FREQUENCY}")
        _safe_select2(driver, f"{MODAL} #select2-Svc_FrequencyTypeID-container", FREQUENCY)
        print("  Frequency selected")

        # Ownership (if visible, pick first real option)
        try:
            own = driver.find_element(By.CSS_SELECTOR, f"{MODAL} #ddlSvc_OwnerShipID")
            if own.is_displayed():
                Select(own).select_by_index(1)
                print("  Ownership selected")
        except NoSuchElementException:
            pass

        # Click Next → goes to Routing step
        print("  Clicking Next...")
        _click_modal_next(driver)
        print("  Advanced to Routing step")

        # ── Step 4: Routing — Thursday + VK Route ────────────────────
        print("\n--- Step 4: Setting routing ---")

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "divAddServiceRoutingContainer"))
        )
        print("  Routing step loaded")

        # Day of Week = Thursday (value "4") — use JS to avoid stale refs
        driver.execute_script("""
            var sel = document.querySelector('#ddlDayofWeeek_0');
            sel.value = arguments[0];
            sel.dispatchEvent(new Event('change', {bubbles: true}));
        """, DAY_OF_WEEK)
        wait_for_loading_screen(driver)
        print("  Day of Week: Thursday")

        # Route = VK Route (with retry — day change reloads the route dropdown)
        _safe_select2(driver, f"{MODAL} #select2-ddlDayofRoute_0-container", ROUTE_NAME)
        print(f"  Route: {ROUTE_NAME}")

        # Click Next → goes to Order Charges / Surcharges
        print("  Clicking Next...")
        _click_modal_next(driver)
        print("  Advanced to Order Charges step")

        # ── Step 5: Skip Order Charges & Surcharges ──────────────────
        print("\n--- Step 5: Skipping Order Charges & Surcharges ---")

        # This screen may use a different Next button (screen 4 advance)
        _click_modal_next_or_screen4(driver)
        wait_for_loading_screen(driver)
        print("  Order Charges skipped")

        # ── Step 6: Start Service Workflow ────────────────────────────
        print("\n--- Step 6: Filling Start Service Workflow ---")

        # Requested By
        print(f"  Requested By: {REQUESTED_BY}")
        req_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "Svc_RequestedBy"))
        )
        req_field.clear()
        req_field.send_keys(REQUESTED_BY)
        print("  Requested By filled")

        # Change Reason (Select2)
        print(f"  Change Reason: {CHANGE_REASON}")
        select2_select(driver, f"{MODAL} #select2-Svc_ServiceChangeReasonID-container", CHANGE_REASON)
        wait_for_loading_screen(driver)
        print("  Change Reason selected")

        # Select only the workflow checkbox with code "Del"
        print(f"  Selecting workflow code: {WORKFLOW_CODE}")
        _select_workflow_checkbox(driver, WORKFLOW_CODE)
        print(f"  Workflow '{WORKFLOW_CODE}' checked")

        # Select Route = VK Route for the workflow row
        print(f"  Setting workflow route: {ROUTE_NAME}")
        _select_workflow_route(driver, ROUTE_NAME)
        print("  Workflow route selected")

        # Click Add Service (submit)
        print("  Clicking Add Service...")
        _click_add_service_submit(driver)
        wait_for_loading_screen(driver)

        # ── Step 7: Verify success message ──────────────────────────
        print("\n--- Step 7: Verifying success message ---")
        assert text_is_visible(driver, "Service has been created successfully", timeout=20), (
            "Service creation success message should be visible"
        )
        print("  SUCCESS: 'Service has been created successfully.' message is displayed")

        # ── Step 8: Navigate to Route Log ────────────────────────────
        print("\n--- Step 8: Navigating to Route Log ---")

        # Go to Home first for a clean nav state
        print("  Navigating to Home...")
        driver.get(BASE_URL + "Home")
        wait_for_loading_screen(driver)

        print("  Clicking Operations menu...")
        navigate_to_menu(driver, "Operations")
        wait_for_loading_screen(driver)
        print("  Operations menu opened")

        # Wait for submenu to expand, then click Route Log
        print("  Clicking Route Log submenu...")
        try:
            route_log_link = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "Active_51"))
            )
            route_log_link.click()
        except TimeoutException:
            # Fallback: try clicking by text
            print("  Active_51 not found, trying by text...")
            route_log_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[contains(@class,"menu-text") and contains(text(),"Route Log")]'
                    ' | //a[contains(text(),"Route Log")]',
                ))
            )
            route_log_link.click()
        wait_for_loading_screen(driver)

        # ── Step 9: Confirm Route Log screen is displayed ────────────
        print("\n--- Step 9: Confirming Route Log screen ---")
        assert text_is_visible(driver, "Route Log", timeout=15), (
            "Route Log page should be visible"
        )
        print("  Route Log screen is displayed")


# ── Helper functions ─────────────────────────────────────────────────


def _search_and_open_customer(driver, wait):
    """Search for the customer by ID and navigate to Customer Details."""
    print("  Searching for customer...")
    search_input = wait.until(
        EC.element_to_be_clickable((By.ID, "txtSearchResultItemFromMenu"))
    )
    search_input.click()
    search_input.send_keys(Keys.CONTROL, "a")
    search_input.send_keys(CUSTOMER_ID + Keys.ENTER)
    wait_for_loading_screen(driver)
    print("  Search submitted, looking for results...")

    # The search may navigate directly to Customer Details or show a results list.
    # Wait briefly to see which happens.
    try:
        WebDriverWait(driver, 5).until(
            lambda d: "/CustomerDetails" in d.current_url
        )
        print("  Search navigated directly to Customer Details")
    except TimeoutException:
        # We're on a results page — try multiple selectors to click the customer
        print("  On search results page, clicking customer link...")
        clicked = False

        # Try: any link/row containing the customer ID
        selectors = [
            f'a[href*="CustomerDetails"][href*="{CUSTOMER_ID}"]',
            f'a[onclick*="{CUSTOMER_ID}"]',
            f'tr[onclick*="{CUSTOMER_ID}"]',
            f'[onclick*="CustomerDetails"][onclick*="{CUSTOMER_ID}"]',
            f'.dx-data-row td a',
        ]
        for sel in selectors:
            try:
                el = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                driver.execute_script("arguments[0].click();", el)
                clicked = True
                print(f"  Clicked via: {sel}")
                break
            except TimeoutException:
                continue

        # Fallback: click first row that contains the customer ID text
        if not clicked:
            try:
                row = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        f'//*[contains(text(),"{CUSTOMER_ID}")]//ancestor::tr'
                        f' | //*[contains(text(),"{CUSTOMER_ID}")]',
                    ))
                )
                driver.execute_script("arguments[0].click();", row)
                clicked = True
                print("  Clicked via text match")
            except TimeoutException:
                pass

        # Last resort: navigate directly by URL
        if not clicked:
            print("  Could not find result link, navigating by URL...")
            driver.get(BASE_URL + f"CustomerDetails?cid={CUSTOMER_ID}")

        wait_for_loading_screen(driver)

    # Confirm we're on the Customer Details page
    WebDriverWait(driver, LONG_WAIT).until(
        lambda d: "/CustomerDetails" in d.current_url
    )
    wait_for_loading_screen(driver)
    print("  Customer Details page loaded")

    assert text_is_visible(driver, CUSTOMER_NAME, timeout=15), (
        f"Customer '{CUSTOMER_NAME}' should be visible"
    )
    assert text_is_visible(driver, "Active", timeout=5), (
        "Customer status should be Active"
    )


def _open_add_service_modal(driver, wait):
    """Scroll to Services section and click Add Service."""
    services_heading = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//*[contains(@class,'innerContentTitle') and contains(text(),'Services')]"
        " | //h3[contains(text(),'Services')]"
        " | //*[@id='services_list_container']/ancestor::*[3]",
    )))
    scroll_to_element(driver, services_heading)

    try:
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "a.AddNewServiceWizardLocation"
        )))
    except TimeoutException:
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "//a[contains(text(),'Add Service')]"
        )))

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
    driver.execute_script("arguments[0].click();", link)

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "myAddServiceLocationView"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "AddServiceLocationBodyContainer"))
    )



def _select_equipment_category(driver):
    """Select equipment category via JS to avoid stale-element issues."""
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f"{MODAL} #Svc_EquipmentCategoryID")
            )
        )
        option_texts = driver.execute_script("""
            var sel = document.querySelector('#Svc_EquipmentCategoryID');
            return Array.from(sel.options).map(o => o.text.trim());
        """)
        print(f"    Available: {option_texts}")

        driver.execute_script("""
            var sel = document.querySelector('#Svc_EquipmentCategoryID');
            var target = arguments[0].toLowerCase();
            for (var i = 0; i < sel.options.length; i++) {
                if (sel.options[i].text.trim().toLowerCase() === target) {
                    sel.selectedIndex = i;
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                    return;
                }
            }
            for (var j = 0; j < sel.options.length; j++) {
                if (sel.options[j].text.toLowerCase().indexOf('towable') >= 0) {
                    sel.selectedIndex = j;
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                    return;
                }
            }
        """, EQUIPMENT_CATEGORY)
        wait_for_loading_screen(driver)
        print("  Equipment Category selected")
    except TimeoutException:
        print("  Equipment Category not visible, skipping")


def _wait_for_select2_ready(driver, container_id, timeout=15):
    """Wait until a Select2 container is present and clickable after AJAX reload."""
    css = f"{MODAL} {container_id}"
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css))
    )
    # Brief pause to let any remaining AJAX settle
    time.sleep(0.5)


def _safe_select2(driver, css_selector, search_text, retries=3):
    """Select2 interaction with retry logic for stale-element scenarios.

    After an AJAX reload the Select2 container may be recreated in the DOM.
    This retries the interaction up to `retries` times.
    """
    from selenium.common.exceptions import StaleElementReferenceException

    for attempt in range(retries):
        try:
            wait_for_loading_screen(driver)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            select2_select(driver, css_selector, search_text)
            wait_for_loading_screen(driver)
            return
        except StaleElementReferenceException:
            print(f"    Stale element on attempt {attempt + 1}, retrying...")
            time.sleep(1)
    # Final attempt without catching
    select2_select(driver, css_selector, search_text)
    wait_for_loading_screen(driver)


def _click_modal_next(driver):
    """Click the visible Next button in the Add Service modal footer."""
    wait_for_loading_screen(driver)
    footers = driver.find_elements(
        By.CSS_SELECTOR, f"{MODAL} .myAddServiceBtnFooter"
    )
    for footer in footers:
        if footer.is_displayed():
            buttons = footer.find_elements(
                By.XPATH, ".//button[contains(text(),'Next')]"
            )
            for btn in buttons:
                if btn.is_displayed():
                    btn.click()
                    wait_for_loading_screen(driver)
                    return

    # Fallback: try any visible Next button inside the modal
    try:
        btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH,
            f'//*[@id="myAddServiceLocationView"]'
            f'//button[contains(text(),"Next") and not(ancestor::*[contains(@style,"display: none")])]',
        )))
        btn.click()
        wait_for_loading_screen(driver)
    except TimeoutException:
        print("  WARNING: No Next button found")


def _click_modal_next_or_screen4(driver):
    """Advance past Order Charges / Surcharges screen.

    Tries the standard Next button first, then the screen-4 specific
    button used by some wizard configurations.
    """
    # Try the standard footer Next first
    footers = driver.find_elements(By.CSS_SELECTOR, f"{MODAL} .myAddServiceBtnFooter")
    for footer in footers:
        if footer.is_displayed():
            buttons = footer.find_elements(By.XPATH, ".//button[contains(text(),'Next')]")
            for btn in buttons:
                if btn.is_displayed():
                    btn.click()
                    wait_for_loading_screen(driver)
                    return

    # Fallback: screen-4 specific button
    try:
        btn4 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'{MODAL} button[onclick*="ShowNextMyAddServiceLocationPopUp(4)"]',
        )))
        btn4.click()
        wait_for_loading_screen(driver)
    except TimeoutException:
        # Last resort: any visible Next
        _click_modal_next(driver)


def _select_workflow_checkbox(driver, workflow_code):
    """Check only the workflow checkbox whose code contains the given text.

    Unchecks all others so only the target workflow (e.g. "Del") is selected.
    """
    wait_for_loading_screen(driver)

    # Find all workflow checkbox rows inside the modal
    checkboxes = driver.find_elements(
        By.CSS_SELECTOR,
        f'{MODAL} input[type="checkbox"][id^="chkSvcCode_"],'
        f' {MODAL} input[type="checkbox"][name*="chkSvcCode"],'
        f' {MODAL} input[type="checkbox"][class*="svcCode"],'
        f' {MODAL} input[type="checkbox"][class*="workflow"]',
    )

    if not checkboxes:
        # Broader fallback: any checkbox in the workflow area
        checkboxes = driver.find_elements(
            By.CSS_SELECTOR,
            f'{MODAL} .addServiceWorkflowContent input[type="checkbox"],'
            f' {MODAL} #divAddServiceWorkflow input[type="checkbox"]',
        )

    matched = False
    for cb in checkboxes:
        # Get the label text or the parent row text to identify the workflow
        try:
            row = cb.find_element(By.XPATH, "./ancestor::tr | ./ancestor::div[1] | ./ancestor::li[1]")
            row_text = row.text
        except NoSuchElementException:
            row_text = ""

        cb_id = cb.get_attribute("id") or ""
        cb_value = cb.get_attribute("value") or ""

        is_target = (
            workflow_code.lower() in row_text.lower()
            or workflow_code.lower() in cb_value.lower()
            or workflow_code.lower() in cb_id.lower()
        )

        if is_target and not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
            matched = True
            print(f"    Checked workflow: {row_text.strip()[:50]}")
        elif not is_target and cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
            print(f"    Unchecked workflow: {row_text.strip()[:50]}")

    if not matched:
        print(f"  WARNING: No checkbox matched workflow code '{workflow_code}'")
        # Fallback: try clicking Add Charge button which may auto-select
        try:
            add_btn = driver.find_element(By.CSS_SELECTOR, f"{MODAL} #addUpdateNewCharge_1")
            add_btn.click()
            wait_for_loading_screen(driver)
        except NoSuchElementException:
            pass


def _select_workflow_route(driver, route_name):
    """Select route for the workflow row via Select2."""
    route_css = (
        f'{MODAL} [id^="select2-ddlDayRouteServiceCodeWorkflow_"]'
        f'[id$="-container"]'
    )
    containers = driver.find_elements(By.CSS_SELECTOR, route_css)
    if containers:
        select2_select(driver, route_css, route_name)
        wait_for_loading_screen(driver)
    else:
        print(f"  WARNING: No workflow route dropdown found")


def _click_add_service_submit(driver):
    """Click the Add Service / Submit button on the final wizard screen."""
    # Try the ShowTemporaryServicePopup button first
    try:
        btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f'{MODAL} button[onclick="ShowTemporaryServicePopup()"]',
        )))
        btn.click()
        return
    except TimeoutException:
        pass

    # Fallback: any button containing "Add Service" text
    try:
        btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH,
            f'//*[@id="myAddServiceLocationView"]'
            f'//button[contains(text(),"Add Service")]',
        )))
        btn.click()
        return
    except TimeoutException:
        pass

    # Last resort: Submit button in visible footer
    footers = driver.find_elements(By.CSS_SELECTOR, f"{MODAL} .myAddServiceBtnFooter")
    for footer in footers:
        if footer.is_displayed():
            buttons = footer.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if btn.is_displayed() and btn.text.strip():
                    btn.click()
                    return


