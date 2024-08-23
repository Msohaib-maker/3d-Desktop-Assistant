import pyautogui
import pygetwindow as gw
from PIL import Image

def capture_current_window():
    # Get the currently active window
    active_window = gw.getActiveWindow()
    if active_window:
        # Capture the area of the active window
        screenshot = pyautogui.screenshot(region=(active_window.left, active_window.top, active_window.width, active_window.height))
        return screenshot
    else:
        print("No active window found.")
        return None

def capture_full_screen():
    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    return screenshot


def show_screenshot(image):
    if image:
        image.show()
    else:
        print("No image to show.")

