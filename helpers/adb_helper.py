import re
import subprocess

from config.settings import DEVICE_UDID


def adb_shell(cmd):
    """Run an ADB shell command on the device."""
    return subprocess.run(
        ["adb", "-s", DEVICE_UDID, "shell"] + cmd,
        capture_output=True,
        text=True,
    )


def adb_type_text(text):
    """Type text via ADB input."""
    adb_shell(["input", "text", text])


def adb_keyevent(keycode, *extra_args):
    """Send a keyevent with optional extra args (e.g. --longpress)."""
    adb_shell(["input", "keyevent", keycode] + list(extra_args))


def adb_clear_field():
    """Select all text in a field and delete it."""
    adb_keyevent("KEYCODE_MOVE_END")
    adb_keyevent("29", "--longpress")  # Ctrl+A equivalent
    adb_keyevent("67")  # Delete


def adb_dismiss_keyboard():
    """Dismiss the on-screen keyboard by pressing Back."""
    adb_keyevent("4")


def adb_tap(x, y):
    """Tap at screen coordinates."""
    adb_shell(["input", "tap", str(x), str(y)])


def adb_find_element_bounds(resource_id):
    """Find element center coordinates via uiautomator dump fallback.

    Returns (x, y) center tuple or None if not found.
    """
    result = subprocess.run(
        ["adb", "-s", DEVICE_UDID, "shell", "uiautomator", "dump", "/dev/tty"],
        capture_output=True,
        text=True,
    )
    escaped_id = re.escape(resource_id)
    match = re.search(
        rf'resource-id="{escaped_id}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
        result.stdout,
    )
    if match:
        x = (int(match.group(1)) + int(match.group(3))) // 2
        y = (int(match.group(2)) + int(match.group(4))) // 2
        return (x, y)
    return None
