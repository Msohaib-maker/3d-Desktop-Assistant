from .action_performer import *

def translate_action(quoted_words):
    # Convert all words to lowercase for consistency
    quoted_words = [word.strip("'").lower() for word in quoted_words]

    # Determine the action: 'open' or 'close'
    action = None
    if 'open' in quoted_words:
        action = 'open'
    elif 'close' in quoted_words:
        action = 'close'

    # List to keep track of applications to act upon
    applications = []

    # Identify all applications mentioned in the quoted words
    for word in quoted_words:
        if not word in ["open", "close"]:
            applications.append(word)

    # Perform the corresponding action for each application
    if action and applications:
        for app in applications:
            if action == 'open':
                if app == "notepad":
                    open_notepad()
                elif app in ["chrome", "browser"]:
                    open_browser()
                elif app in ["file explorer", "explorer"]:
                    open_file_explorer()
                else:
                    open_app(app)
            elif action == 'close':
                if app == "notepad":
                    close_app()
                elif app in ["chrome", "browser"]:
                    close_browser()
                elif app in ["file explorer", "explorer"]:
                    close_file_explorer()
                else:
                    close_app(app)
    else:
        print("No valid action or application found.")


def close_file_explorer():
    """
    Close all instances of Windows File Explorer (explorer.exe).
    """
    # File Explorer process name
    process_name = 'explorer.exe'

    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                proc.terminate()  # or proc.kill() for forceful termination
                print("Closed File Explorer.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass