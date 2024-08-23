from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_twitter():
    # Set up Chrome WebDriver
    option = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Open Twitter
        driver.get("https://twitter.com")
        
        # Wait for the page to load
        time.sleep(2)
        
    finally:
        # Optionally, keep the browser open or close it
        # driver.quit()
        pass

# Example usage
