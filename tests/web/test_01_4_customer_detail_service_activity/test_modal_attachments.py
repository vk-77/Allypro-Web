"""
Customer Details - Service Activity tab - work order Attachments tab.

"""
import os
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.web.customer_page import CustomerPage
from helpers.web_helper import wait_for_loading_screen, force_click
from config.web_settings import DEFAULT_WAIT


def _open_attachments_tab(driver):
    """Open today's work order and activate the Attachments tab."""
    page = CustomerPage(driver)
    page.open_work_order_modal_tab(page.WO_TAB_ATTACHMENTS, page.WO_PANE_ATTACHMENTS)
    wait_for_loading_screen(driver)
    return page


@pytest.mark.usefixtures("driver")
class TestModalAttachments:
    """
    Service Activity tab - work order Attachments tab.

    """

    def test_c339628_attachments_tab_four_panel_titles(self, driver):
        """C339628 Attachments tab: Verify four panel titles are present."""
        page = _open_attachments_tab(driver)
        pane = page.find_visible(By.ID, "woChildTabContainerOrder_5", timeout=15)
        # Order Note
        order_note = pane.find_element(
            By.XPATH, './/strong[contains(text(),"Order Note")]'
        )
        assert order_note is not None
        # Operations Response
        ops_response = pane.find_element(
            By.XPATH, './/strong[contains(text(),"Operations Response")]'
        )
        assert ops_response is not None
        # Signature
        signature = pane.find_element(
            By.XPATH, './/strong[text()="Signature"]'
        )
        assert signature is not None
        # Attachments
        attachments = pane.find_element(
            By.XPATH, './/strong[text()="Attachments"]'
        )
        assert attachments is not None

    def test_c339629_attachments_tab_signature_required_toggle(self, driver):
        """C339629 Attachments tab: Verify Signature Required toggle changes checked state."""
        page = _open_attachments_tab(driver)
        chk = page.find_element(*page.WO_SIGNATURE_REQUIRED)
        initial = chk.is_selected()
        force_click(driver, *page.WO_SIGNATURE_REQUIRED)
        chk = page.find_element(*page.WO_SIGNATURE_REQUIRED)
        assert chk.is_selected() != initial
        # Toggle back
        force_click(driver, *page.WO_SIGNATURE_REQUIRED)
        chk = page.find_element(*page.WO_SIGNATURE_REQUIRED)
        assert chk.is_selected() == initial

    def test_c339630_attachments_tab_image_required_toggle(self, driver):
        """C339630 Attachments tab: Verify Image Required toggle changes checked state."""
        page = _open_attachments_tab(driver)
        chk = page.find_element(*page.WO_IMAGE_REQUIRED)
        initial = chk.is_selected()
        force_click(driver, *page.WO_IMAGE_REQUIRED)
        chk = page.find_element(*page.WO_IMAGE_REQUIRED)
        assert chk.is_selected() != initial
        # Toggle back
        force_click(driver, *page.WO_IMAGE_REQUIRED)
        chk = page.find_element(*page.WO_IMAGE_REQUIRED)
        assert chk.is_selected() == initial

    def test_c339631_attachments_tab_add_file_functionality(self, driver):
        """C339631 Attachments tab: Verify Add File functionality."""
        page = _open_attachments_tab(driver)
        # Verify Add File wrap is visible
        wrap = page.find_visible(*page.WO_ATTACHMENT_ADD_FILE_WRAP)
        assert wrap.is_displayed()
        # Verify "Add File" span exists
        add_file_span = driver.find_element(
            By.XPATH, '//span[contains(@class,"small_anchor_btn") and contains(text(),"Add File")]'
        )
        assert add_file_span is not None
        # Attach a file
        file_input = page.find_element(*page.WO_ADD_ORDER_ATTACHMENT_FILE)
        sample_path = os.path.join(os.path.dirname(__file__), "sample-upload.png")
        if not os.path.exists(sample_path):
            import struct, zlib
            def _minimal_png():
                sig = b'\x89PNG\r\n\x1a\n'
                ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
                ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
                ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
                raw = b'\x00\x00\x00\x00'
                idat_data = zlib.compress(raw)
                idat_crc = zlib.crc32(b'IDAT' + idat_data) & 0xffffffff
                idat = struct.pack('>I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('>I', idat_crc)
                iend_crc = zlib.crc32(b'IEND') & 0xffffffff
                iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
                return sig + ihdr + idat + iend
            with open(sample_path, 'wb') as f:
                f.write(_minimal_png())
        file_input.send_keys(sample_path)
        # Verify file was attached
        value = file_input.get_attribute("value")
        assert "sample-upload.png" in value.lower()
        wait_for_loading_screen(driver)
