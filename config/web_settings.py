"""
Web application settings for Elements browser testing.
"""
import os

# Base URL
BASE_URL = os.environ.get(
    "ELEMENTS_BASE_URL", "https://stage.elements.rwgstage.com/"
)

# Browser (chrome, edge, firefox)
BROWSER = os.environ.get("ELEMENTS_BROWSER", "chrome")
HEADLESS = os.environ.get("ELEMENTS_HEADLESS", "false").lower() == "true"

# Timeouts (seconds)
DEFAULT_WAIT = 10
PAGE_LOAD_TIMEOUT = 90
LOADING_SCREEN_TIMEOUT = 130

# Viewport
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 1000

# Credentials
COMPANY = os.environ.get("ELEMENTS_COMPANY", "allypro")
USERNAME = os.environ.get("ELEMENTS_USER", "sparks@routeware.com")
PASSWORD = os.environ.get("ELEMENTS_PASS", "@llyPro$")

# Supervisor credentials
SUPERVISOR_COMPANY = os.environ.get("ELEMENTS_SUPERVISOR_COMPANY", "allypro")
SUPERVISOR_USERNAME = os.environ.get(
    "ELEMENTS_SUPERVISOR_USER", "sparks@routeware.com"
)
SUPERVISOR_PASSWORD = os.environ.get("ELEMENTS_SUPERVISOR_PASS", "@llyPro$")
