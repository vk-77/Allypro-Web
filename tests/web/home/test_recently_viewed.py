"""
Home page Recently Viewed section tests.

Validates that the Recently Viewed section is visible on the Home
page and contains customer links for quick navigation.
"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomePage


@pytest.mark.usefixtures("driver")
class TestRecentlyViewed:
    """
    Verify Recently Viewed section on the Home page.

    Usage:
        pytest tests/web/home/test_recently_viewed.py -v
    """

    def test_c70240_verify_recently_viewed_section_visible(self, driver):
        """C70240 Verify Recently Viewed section is visible with customer links."""
        home_page = HomePage(driver)

        assert home_page.text_is_visible("Recently Viewed"), (
            "Recently Viewed section title should be visible on the Home page"
        )

        # Verify the section container is present
        section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Recently Viewed')]/"
                 "ancestor::*[contains(@class,'widget') or "
                 "contains(@class,'card') or contains(@class,'panel')]")
            )
        )
        assert section.is_displayed(), (
            "Recently Viewed section container should be visible"
        )

        # Verify customer links exist within the section
        links = section.find_elements(By.CSS_SELECTOR, "a")
        assert len(links) > 0, (
            "Recently Viewed section should contain customer links"
        )
