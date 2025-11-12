"""
Page object for the Elements web login screen.
"""
from selenium.webdriver.common.by import By

from .base_web_page import BaseWebPage


class WebLoginPage(BaseWebPage):
    """
    Page object representing the Elements Login screen.

    Locators and actions for company, email, password fields and login button.
    """

    # ── Locators ──────────────────────────────────────────────────

    ELEMENTS_LOGO = (By.CSS_SELECTOR, '[src="/Images/AllyPro-icon.svg"]')
    LOGIN_BOX_LOGO = (By.CSS_SELECTOR, ".admin-form-main-title-image img")
    TITLE_TEXT = "Please enter your company, email and password"

    COMPANY_FIELD = (By.ID, "CompanyName")
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "EncryptedPassword")
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".custom_login_btn")

    EULA_TEXT = "By logging in, user is agreeing to terms in EULA."
    EULA_MODAL = (By.ID, "modalAggrementPopup")
    EULA_IFRAME = (By.ID, "iframeRNotes")
    EULA_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        '#modalAggrementPopup button.close.closeBtn, '
        '#modalAggrementPopup button[data-dismiss="modal"]',
    )

    COPYRIGHT_FOOTER = (By.CSS_SELECTOR, ".admin-form-footer a")

    # ── Actions ───────────────────────────────────────────────────

    def enter_company(self, company):
        """Enter text into the Company field."""
        self.type_text(*self.COMPANY_FIELD, company)

    def enter_email(self, email):
        """Enter text into the Email field."""
        self.type_text(*self.EMAIL_FIELD, email)

    def enter_password(self, password):
        """Enter text into the Password field."""
        self.type_text(*self.PASSWORD_FIELD, password)

    def click_login(self):
        """Click the Login button."""
        self.click_element(*self.LOGIN_BUTTON)

    def fill_login_form(self, company=None, email=None, password=None):
        """
        Fill login form fields. Skips any field that is None.

        Args:
            company: Company name (optional)
            email: Email address (optional)
            password: Password (optional)
        """
        if company:
            self.enter_company(company)
        if email:
            self.enter_email(email)
        if password:
            self.enter_password(password)

    def attempt_login(self, company=None, email=None, password=None):
        """
        Fill login form and click the login button.

        Args:
            company: Company name (optional)
            email: Email address (optional)
            password: Password (optional)
        """
        self.fill_login_form(company, email, password)
        self.click_login()

    def login(self, company, email, password):
        """
        Complete login flow: fill all fields, click login, wait for loading.

        Args:
            company (str): Company name
            email (str): Email address
            password (str): Password
        """
        self.attempt_login(company, email, password)
        self.wait_for_loading_screen()

    # ── Assertions / queries ──────────────────────────────────────

    def is_elements_logo_visible(self):
        """Return True if Elements logo is visible."""
        return self.element_is_visible(*self.ELEMENTS_LOGO)

    def is_login_box_logo_visible(self):
        """Return True if login box logo is visible."""
        return self.element_is_visible(*self.LOGIN_BOX_LOGO)

    def is_title_visible(self):
        """Return True if the login title text is visible."""
        return self.text_is_visible(self.TITLE_TEXT)

    def is_company_field_visible(self):
        """Return True if Company field is visible and enabled."""
        el = self.find_visible(*self.COMPANY_FIELD)
        return el.is_displayed() and el.is_enabled()

    def is_email_field_visible(self):
        """Return True if Email field is visible and enabled."""
        el = self.find_visible(*self.EMAIL_FIELD)
        return el.is_displayed() and el.is_enabled()

    def is_password_field_visible(self):
        """Return True if Password field is visible, enabled, and type=password."""
        el = self.find_visible(*self.PASSWORD_FIELD)
        return (
            el.is_displayed()
            and el.is_enabled()
            and el.get_attribute("type") == "password"
        )

    def is_login_button_visible(self):
        """Return True if Login button is visible and enabled."""
        el = self.find_visible(*self.LOGIN_BUTTON)
        return el.is_displayed() and el.is_enabled()

    def get_password_field_type(self):
        """Return the type attribute of the password field."""
        return self.get_attribute(*self.PASSWORD_FIELD, "type")

    def get_password_field_value(self):
        """Return the value of the password field."""
        return self.get_attribute(*self.PASSWORD_FIELD, "value")

    def open_eula_modal(self):
        """Click the EULA text to open the EULA modal."""
        # Use JavaScript to find and click the element containing EULA text,
        # which is more reliable than XPath when text spans child elements.
        self.driver.execute_script("""
            var elements = document.querySelectorAll('*');
            for (var i = 0; i < elements.length; i++) {
                var el = elements[i];
                if (el.children.length === 0 || el.tagName === 'A' || el.tagName === 'SPAN') {
                    if (el.textContent.includes('EULA') && el.offsetParent !== null) {
                        el.click();
                        return;
                    }
                }
            }
            // Fallback: click any element with the full text
            for (var j = 0; j < elements.length; j++) {
                if (elements[j].textContent.includes('agreeing to terms in EULA')) {
                    elements[j].click();
                    return;
                }
            }
        """)

    def is_eula_modal_visible(self):
        """Return True if the EULA modal is visible."""
        return self.element_is_visible(*self.EULA_MODAL)

    def close_eula_modal(self):
        """Close the EULA modal via the X button."""
        self.click_element(*self.EULA_CLOSE_BUTTON)

    def get_eula_iframe_content(self):
        """Switch into EULA iframe and return the h1 text."""
        iframe = self.find_element(*self.EULA_IFRAME)
        self.driver.switch_to.frame(iframe)
        h1 = self.find_element(By.CSS_SELECTOR, "h1.h2.text-center")
        text = h1.text
        self.driver.switch_to.default_content()
        return text

    def get_copyright_text(self):
        """Return copyright footer text."""
        return self.get_text(*self.COPYRIGHT_FOOTER)

    def get_icon_in_parent(self, field_locator, icon_keywords):
        """
        Check if an icon (svg, img, or class-based) exists next to a field.

        Args:
            field_locator: Tuple (By, value) for the input field.
            icon_keywords: List of keyword strings to search for.

        Returns:
            True if any matching icon is found.
        """
        field = self.find_element(*field_locator)
        parent = field.find_element(By.XPATH, "..")
        for keyword in icon_keywords:
            selectors = [
                "svg",
                f'[class*="{keyword}"]',
                f'img[alt*="{keyword}"]',
            ]
            for sel in selectors:
                elements = parent.find_elements(By.CSS_SELECTOR, sel)
                if any(el.is_displayed() for el in elements):
                    return True
        return False
