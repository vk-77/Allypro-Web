"""
Home - Digital Documents widget tests.

"""
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.home_web_page import HomeWebPage


@pytest.mark.usefixtures("driver")
class TestDigitalDocuments:
    """
    Verify Digital Documents widget on the Home page.

    Usage:
        pytest tests/web/test_10_home/test_04_digital_documents.py -v
    """

    def test_c70201_verify_digital_documents_widget_visible(self, driver):
        """C70201 Verify Digital Documents widget is visible with headers."""
        home_page = HomeWebPage(driver)

        assert home_page.text_is_visible("Digital Documents"), (
            "Digital Documents widget title should be visible on the Home page"
        )

        # Verify the widget section/container is present
        widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//*[contains(text(),'Digital Documents')]/ancestor::*["
                 "contains(@class,'widget') or contains(@class,'card') "
                 "or contains(@class,'panel')]")
            )
        )
        assert widget.is_displayed(), (
            "Digital Documents widget container should be visible"
        )
