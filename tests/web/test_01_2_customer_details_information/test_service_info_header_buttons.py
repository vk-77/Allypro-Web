"""
Customer Details - Service Info header buttons tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.web.base_web_page import BaseWebPage
from pages.web.customer_page import CustomerPage
from helpers.web_helper import (
    wait_for_loading_screen,
    select2_select,
    scroll_to_element,
    force_click,
)
from data.user_data import USER_DATA


@pytest.mark.usefixtures("driver")
class TestServiceInfoHeaderButtons:
    """
    Service Info header button tests.

    Usage:
        pytest tests/web/test_01_2_customer_details_information/test_service_info_header_buttons.py -v
    """

    def test_c70538_info_icon_opens_dropdown_with_service_ids(self, driver):
        """C70538 Service Info header - Info (i) icon opens dropdown displaying Service ID and Service UID."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.select_first_service()

        # Ensure Services section is visible
        content = driver.find_element(By.ID, "content")
        services_el = content.find_element(By.XPATH, ".//*[contains(text(),'Services')]")
        scroll_to_element(driver, services_el)
        assert services_el.is_displayed()

        # Check if customer has services
        service_items = driver.find_elements(
            By.CSS_SELECTOR, "#services_list_container li:not(.no-services)"
        )
        if len(service_items) == 0:
            return

        # Click Service Info heading to expand
        heading = page.get_service_info_heading()
        if heading:
            scroll_to_element(driver, heading)
            driver.execute_script("arguments[0].click();", heading)
            WebDriverWait(driver, 6).until(lambda d: True)

        # Get Service Info panel and click info icon
        panel = page._get_service_info_panel(heading)
        info_icon = panel.find_element(
            By.CSS_SELECTOR, 'a.servicemapicon.dropdown-toggle[data-toggle="dropdown"]'
        )
        assert info_icon.is_displayed()
        info_icon.click()

        # Assert dropdown shows ServiceID and ServiceUID with clipboard icons
        troubleshoot = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#troubleshootids.dropdown-menu"))
        )
        assert troubleshoot.is_displayed()

        ul = troubleshoot.find_element(By.CSS_SELECTOR, "ul")
        assert ul.is_displayed()

        lis = ul.find_elements(By.CSS_SELECTOR, "li")
        li_texts = [li.text for li in lis]
        assert any("ServiceID:" in t for t in li_texts), "ServiceID: should be present"
        assert any("ServiceUID:" in t for t in li_texts), "ServiceUID: should be present"

        clipboard_icons = ul.find_elements(By.CSS_SELECTOR, "i.fa-clipboard")
        assert len(clipboard_icons) >= 2, "Should have at least 2 clipboard icons"

    def test_c67604_add_order(self, driver):
        """C67604 Add Order."""
        page = CustomerPage(driver)
        wait = WebDriverWait(driver, 15)

        page.add_new_service_from_customer_details()

        # Click center_li_1
        center_li = wait.until(
            EC.element_to_be_clickable((By.ID, "center_li_1"))
        )
        center_li.click()

        # Click element with onclick containing ", 2, 0)"
        add_order_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[onclick*=", 2, 0)"]'))
        )
        add_order_btn.click()
        wait_for_loading_screen(driver)

        # Verify "New Order for" is visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, "//*[contains(text(),'New Order for')]"
            ))
        )

        # Fill Request By
        req_by = wait.until(
            EC.visibility_of_element_located((By.ID, "order_RequestBy"))
        )
        req_by.clear()
        req_by.send_keys("Test User")

        # Select Order Type
        order_type_btn = driver.find_element(By.CSS_SELECTOR, '[title="Select order type"]')
        order_type_btn.click()
        bulk_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//*[@id='select2-order_Type-results']//*[contains(text(),'BULK PICKUP - Bulk')]"
            ))
        )
        bulk_option.click()

        # Select Route
        route_btn = driver.find_element(By.CSS_SELECTOR, '[title="Select Route"]')
        route_btn.click()
        search_field = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[class*="-search__field"]'))
        )
        search_field.send_keys("cl")
        search_field.send_keys(Keys.ENTER)

        # Handle Destination dropdown if visible
        try:
            dest_dropdown = driver.find_element(By.ID, "destinationDropdown")
            if dest_dropdown.is_displayed():
                dest_btn = driver.find_element(By.CSS_SELECTOR, '[title="Select Destination"]')
                dest_btn.click()
                dest_search = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '[class*="-search__field"]'))
                )
                dest_search.send_keys("QA")
                dest_search.send_keys(Keys.ENTER)
        except (NoSuchElementException, TimeoutException):
            pass

        # Save order charges if available
        try:
            save_charges_btns = driver.find_elements(
                By.XPATH,
                "//*[self::button or self::a or self::input[@type='submit']]"
                "[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save') and "
                "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'charge')]"
            )
            if save_charges_btns:
                driver.execute_script("arguments[0].click();", save_charges_btns[0])
                wait_for_loading_screen(driver)
        except NoSuchElementException:
            pass

        # Click Create Order
        create_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "btnCreateServiceOrder"))
        )
        create_btn.click()
        wait_for_loading_screen(driver)

        # Verify success message
        success = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "divSucessContent"))
        )
        assert "Order has been inserted successfully" in success.text
