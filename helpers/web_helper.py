"""
Web helper utilities for Elements browser testing.

Provides reusable functions for common operations like menu navigation,
Select2 dropdown interaction, date range selection, and grid operations.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from config.web_settings import DEFAULT_WAIT, LOADING_SCREEN_TIMEOUT


LOADING_SCREEN_SELECTOR = "[class^='progressImage']"


def wait_for_loading_screen(driver, timeout=None):
    """Wait until the loading screen (progressImage) is gone."""
    timeout = timeout or LOADING_SCREEN_TIMEOUT
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: not _is_loader_visible(d)
        )
    except TimeoutException:
        pass


def _is_loader_visible(driver):
    """Return True if loading overlay is currently visible."""
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, LOADING_SCREEN_SELECTOR)
        return any(el.is_displayed() for el in elements)
    except StaleElementReferenceException:
        return False


def navigate_to_menu(driver, menu_text):
    """Click a top-level menu item by its visible text."""
    wait = WebDriverWait(
        driver, DEFAULT_WAIT,
        ignored_exceptions=[StaleElementReferenceException],
    )
    menu = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f'//*[contains(@class,"menu-text") and contains(normalize-space(.),"{menu_text}")]'
    )))
    menu.click()


def click_submenu(driver, element_id):
    """Click a submenu item by its ID (e.g., '#Active_66')."""
    wait = WebDriverWait(driver, DEFAULT_WAIT)
    el = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
    el.click()
    wait_for_loading_screen(driver)


def select2_select(driver, container_selector, search_text, timeout=None):
    """
    Interact with a Select2 dropdown: click to open, type search text, press Enter.

    Args:
        driver: WebDriver instance
        container_selector: CSS selector for the Select2 container element
        search_text: Text to type into the search field
        timeout: Optional timeout override
    """
    timeout = timeout or DEFAULT_WAIT
    wait = WebDriverWait(driver, timeout)

    container = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, container_selector)
    ))
    container.click()

    search_field = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, ".select2-container--open input.select2-search__field"
    )))
    search_field.clear()
    search_field.send_keys(search_text)
    search_field.send_keys(Keys.ENTER)


def select2_select_option(driver, container_selector, search_text, option_text, timeout=None):
    """
    Select2 dropdown: open, search, then click a specific option by text.

    Args:
        driver: WebDriver instance
        container_selector: CSS selector for the Select2 container
        search_text: Text to type in search
        option_text: Visible text of the option to click
        timeout: Optional timeout
    """
    timeout = timeout or DEFAULT_WAIT
    wait = WebDriverWait(driver, timeout)

    container = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, container_selector)
    ))
    container.click()

    search_field = wait.until(EC.visibility_of_element_located((
        By.CSS_SELECTOR, ".select2-container--open input.select2-search__field"
    )))
    search_field.clear()
    search_field.send_keys(search_text)

    option = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f'//li[contains(@class,"select2-results__option") and contains(text(),"{option_text}")]'
    )))
    option.click()


def select_dropdown(driver, selector, value):
    """Select an option from a native <select> by value."""
    wait = WebDriverWait(driver, DEFAULT_WAIT)
    el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    Select(el).select_by_value(value)


def select_dropdown_by_index(driver, selector, index):
    """Select an option from a native <select> by index."""
    wait = WebDriverWait(driver, DEFAULT_WAIT)
    el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    Select(el).select_by_index(index)


def select_date_range(driver, selector_from, selector_to, start_date, end_date):
    """
    Set date range using JavaScript (mirrors Cypress selectDateRange command).

    Args:
        driver: WebDriver instance
        selector_from: ID of the from-date input
        selector_to: ID of the to-date input
        start_date: Start date string (MM/DD/YYYY)
        end_date: End date string (MM/DD/YYYY)
    """
    js = """
    var el = document.getElementById(arguments[0]);
    el.value = arguments[1];
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
    """
    driver.execute_script(js, selector_from, start_date)
    driver.execute_script(js, selector_to, end_date)

    # Update the combined display field
    js_combined = """
    var el = document.getElementById(arguments[0]);
    var prev = el.previousElementSibling;
    if (prev) {
        prev.removeAttribute('readonly');
        prev.value = arguments[1] + ' - ' + arguments[2];
        prev.setAttribute('data-date', arguments[1] + ' - ' + arguments[2]);
        prev.dispatchEvent(new Event('input', {bubbles: true}));
        prev.dispatchEvent(new Event('change', {bubbles: true}));
    }
    """
    driver.execute_script(js_combined, selector_from, start_date, end_date)


def clear_session_storage(driver):
    """Clear browser session storage."""
    try:
        driver.execute_script("window.sessionStorage.clear();")
    except Exception:
        pass


def text_is_visible(driver, text, timeout=10):
    """Return True if text is visible anywhere on the page.

    Uses JavaScript innerText for robust matching that handles
    nested elements, whitespace, and avoids stale element issues.
    """
    try:
        WebDriverWait(
            driver, timeout,
            ignored_exceptions=[StaleElementReferenceException],
        ).until(
            lambda d: text.lower() in (
                d.execute_script("return document.body.innerText || '';")
                .lower()
            )
        )
        return True
    except TimeoutException:
        return False


def text_not_present(driver, text, timeout=3):
    """Return True if text is NOT visible on the page."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: text.lower() not in (
                d.execute_script("return document.body.innerText || '';")
                .lower()
            )
        )
        return True
    except TimeoutException:
        return False


def scroll_to_element(driver, element):
    """Scroll element into view."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def force_click(driver, by, value, timeout=None):
    """Click element via JavaScript (force click for hidden/overlapped elements)."""
    timeout = timeout or DEFAULT_WAIT
    wait = WebDriverWait(
        driver, timeout,
        ignored_exceptions=[StaleElementReferenceException],
    )
    el = wait.until(EC.presence_of_element_located((by, value)))
    driver.execute_script("arguments[0].click();", el)
