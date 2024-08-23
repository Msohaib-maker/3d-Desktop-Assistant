import os
import subprocess
import webbrowser
import glob
import psutil
import signal
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import pyautogui
import win32com.client as win32
import time


desktop_apps = []

program_dirs = [
    os.environ.get("ProgramFiles", "C:\\Program Files"),
    os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
    os.environ.get("ProgramW6432", "C:\\Program Files"),
    os.path.expanduser("~\\AppData\\Local\\Programs"),
]

def open_file_explorer():
    os.startfile("C:\\")


def open_notepad():
    # Open Notepad (example for Windows)
    subprocess.Popen(["notepad.exe"])

def open_browser():
    webbrowser.open("https://www.google.com")

def get_all_apps():

    global desktop_apps

    # Path to the desktop directory
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    if len(desktop_apps) == 0:
        # List all files and directories on the desktop
        desktop_apps = os.listdir(desktop_path)
        # for item in desktop_apps:
        #     print(item)


def open_app(app_name : str):
    global desktop_apps

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    if len(desktop_apps) == 0:
        get_all_apps()
    
    for item in desktop_apps:
        if app_name.lower() in item.lower():
            shortcut_path = os.path.join(desktop_path, item)
            if os.path.exists(shortcut_path):
                # Open the application
                subprocess.Popen([shortcut_path], shell=True)
                print(f"Opening {item}...")
                return
            else:
                print(f"Shortcut {item} not found.")
                return
            
    # If not found on desktop, search in program directories
    for directory in program_dirs:
        search_pattern = os.path.join(directory, '**', f'{app_name}.exe')
        exe_files = glob.glob(search_pattern, recursive=True)
        if exe_files:
            subprocess.Popen([exe_files[0]], shell=True)
            print(f"Opening {exe_files[0]} from program directories...")
            return
        
    print(f"Application '{app_name}' not found in your system.")

def close_app(app_name):
    # Iterate over all running processes
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # Check if the process name or executable path matches the app name
            if app_name.lower() in process.info['name'].lower() or \
               (process.info['exe'] and app_name.lower() in os.path.basename(process.info['exe']).lower()):
                os.kill(process.info['pid'], signal.SIGTERM)
                print(f"Closed {process.info['name']} with PID {process.info['pid']}.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    print(f"No open application matching '{app_name}' found.")

def set_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume.iid, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    print(f"Current volume: {current_volume:.0f}%")
    
    try:
        new_volume = float(input("Enter new volume level (0-100): "))
        if 0 <= new_volume <= 100:
            volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
            print(f"Volume set to {new_volume:.0f}%")
        else:
            print("Volume should be between 0 and 100.")
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 100.")


def show_battery_status():
    battery = psutil.sensors_battery()
    
    if battery:
        percent = battery.percent
        plugged_in = battery.power_plugged
        
        print(f"Battery: {percent}%")
        print("Plugged in: Yes" if plugged_in else "Plugged in: No")
    else:
        print("No battery information available.")


def check_and_toggle_wifi():
    try:
        # Check the current WiFi status
        result = subprocess.run(
            ["netsh", "interface", "show", "interface"], 
            capture_output=True, text=True
        )
        output = result.stdout

        # Check if WiFi is connected
        if "Wi-Fi" in output and "Connected" in output:
            print("WiFi is already on.")
        else:
            # Turn WiFi on
            print("Turning WiFi on...")
            subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"], check=True)
            print("WiFi is now on.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def is_process_running(process_name):
    # Check if a process with the given name is running
    for process in psutil.process_iter(['name']):
        if process_name.lower() in process.info['name'].lower():
            return True
    return False

def write_text_in_notepad_or_word(text):
    if is_process_running("notepad.exe"):
        # Type the text into Notepad
        print("notepad")
        pyautogui.write(text, interval=0.1)
        pyautogui.press('enter')
        return

    try:
        word = win32.Dispatch("Word.Application")
        if is_process_running("WINWORD.EXE"):
            # Open Word if it's not running
            # Write the text into Word
            doc = word.ActiveDocument
            selection = word.Selection
            selection.TypeText(text)
            selection.TypeParagraph()
            return

    except Exception as e:
        print(f"An error occurred: {e}")
    
    if not is_process_running("notepad.exe"):
        open_notepad()

        # Type the text into Notepad
        pyautogui.write(text, interval=0.1)
        pyautogui.press('enter')


def close_browser(browser_name):
    """
    Close the specified browser.
    
    :param browser_name: Name of the browser to close (e.g., 'chrome', 'firefox', 'edge')
    """
    # Mapping of browser names to their process names
    browser_processes = {
        'chrome': 'chrome',
        'firefox': 'firefox',
        'edge': 'msedge'
    }

    process_name = browser_processes.get(browser_name.lower())

    if not process_name:
        print(f"Browser '{browser_name}' is not supported.")
        return

    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name in proc.info['name'].lower():
                proc.terminate()  # or proc.kill() for forceful termination
                print(f"Closed {browser_name}.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


