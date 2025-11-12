"""
Base page object for Elements web application (browser).

Provides common Selenium WebDriver actions with CSS/XPath selectors.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from config.web_settings import DEFAULT_WAIT, LOADING_SCREEN_TIMEOUT


class BaseWebPage:
    """
    Base class with common Selenium browser actions:
    - wait for elements
    - click elements
    - type text
    - wait for loading screen
    - clear session storage
    """

    LOADING_SCREEN_SELECTOR = "[class^='progressImage']"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT)

    # ── Element finders ───────────────────────────────────────────

    def find_element(self, by, value, timeout=None):
        """Wait for element presence and return it."""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.presence_of_element_located((by, value)))

    def find_visible(self, by, value, timeout=None):
        """Wait for element to be visible and return it."""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.visibility_of_element_located((by, value)))

    def find_clickable(self, by, value, timeout=None):
        """Wait for element to be clickable and return it."""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.element_to_be_clickable((by, value)))

    def find_elements(self, by, value):
        """Return all matching elements (no wait)."""
        return self.driver.find_elements(by, value)

    def element_exists(self, by, value, timeout=None):
        """Return True if element exists within timeout."""
        timeout = timeout if timeout is not None else DEFAULT_WAIT
        try:
            WebDriverWait(
                self.driver, timeout,
                ignored_exceptions=[StaleElementReferenceException],
            ).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def element_is_visible(self, by, value, timeout=None):
        """Return True if element is visible within timeout."""
        timeout = timeout if timeout is not None else DEFAULT_WAIT
        try:
            WebDriverWait(
                self.driver, timeout,
                ignored_exceptions=[StaleElementReferenceException],
            ).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def element_not_visible(self, by, value, timeout=5):
        """Return True if element is not visible or not present within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    # ── Actions ───────────────────────────────────────────────────

    def click_element(self, by, value, timeout=None):
        """Wait for element to be clickable and click it."""
        self.find_clickable(by, value, timeout).click()

    def type_text(self, by, value, text, clear_first=True):
        """Click field, optionally clear it, and type text."""
        field = self.find_clickable(by, value)
        if clear_first:
            field.clear()
        field.send_keys(text)

    def get_text(self, by, value, timeout=None):
        """Wait for element and return its text content."""
        return self.find_visible(by, value, timeout).text

    def get_attribute(self, by, value, attribute, timeout=None):
        """Wait for element and return an attribute value."""
        return self.find_element(by, value, timeout).get_attribute(attribute)

    # ── Navigation ────────────────────────────────────────────────

    def visit(self, url):
        """Navigate to a URL."""
        self.driver.get(url)

    def current_url(self):
        """Return the current page URL."""
        return self.driver.current_url

    # ── Loading screen ────────────────────────────────────────────

    def wait_for_loading_screen(self, timeout=None):
        """
        Wait until the loading screen (progressImage) is gone.

        Matches Cypress waitForLoadingScreen: passes when the element
        either does not exist in the DOM or is not visible.
        """
        timeout = timeout or LOADING_SCREEN_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: not self._is_loader_visible()
            )
        except TimeoutException:
            pass  # Loader may never appear for fast responses

    def _is_loader_visible(self):
        """Return True if the loading overlay is currently visible."""
        try:
            elements = self.driver.find_elements(
                By.CSS_SELECTOR, self.LOADING_SCREEN_SELECTOR
            )
            return any(el.is_displayed() for el in elements)
        except StaleElementReferenceException:
            return False

    # ── Session / storage ─────────────────────────────────────────

    def clear_session_storage(self):
        """Clear browser sessionStorage."""
        self.driver.execute_script("window.sessionStorage.clear();")

    def clear_local_storage(self):
        """Clear browser localStorage."""
        self.driver.execute_script("window.localStorage.clear();")

    # ── Contains text helpers ─────────────────────────────────────

    def find_by_text(self, text, tag="*", timeout=None):
        """Find element containing text (XPath normalize-space)."""
        escaped = text.replace("'", "\\'")
        xpath = f"//{tag}[contains(normalize-space(.),'{escaped}')]"
        return self.find_visible(By.XPATH, xpath, timeout)

    def text_is_visible(self, text, tag="*", timeout=10):
        """Return True if text is visible anywhere on the page.

        Uses JavaScript innerText for robust matching that handles
        nested elements, whitespace, and avoids stale element issues.
        """
        try:
            WebDriverWait(
                self.driver, timeout,
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

    def text_not_present(self, text, tag="*", timeout=3):
        """Return True if text is NOT visible on the page."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: text.lower() not in (
                    d.execute_script("return document.body.innerText || '';")
                    .lower()
                )
            )
            return True
        except TimeoutException:
            return False
