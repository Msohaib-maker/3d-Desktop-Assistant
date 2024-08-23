import webbrowser, requests, bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import threading

def google_search(search_query):  
    print('Googling...')
    
    # Format the search query for the URL
    url="https://www.google.com/search?btnG=1&q="+search_query
    webbrowser.open(url)


def google_search_and_open_first_link(search_query):
    # Set up Chrome WebDriver with the Service object
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome( options=chrome_options)
    
    
    
    # Open Google
    driver.get("https://www.google.com")

    # Find the search box and enter the query
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(2)  # Adjust the sleep time if necessary

    # Find the first result link and click it
    first_link = driver.find_element(By.CSS_SELECTOR, 'h3')
    first_link.click()

    # Wait for the page to load and then give control back
    time.sleep(2)  # Adjust if necessary
    print("Selenium has navigated to the first link. The browser will remain open.")
    
        

def _setup_chrome_options(download_dir):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,  # Disable download prompt
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # Enable safe browsing
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)
    return chrome_options

def download_file_from_website(search_query, download_dir):
    # Set up Chrome WebDriver with options
    chrome_options = _setup_chrome_options(download_dir)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open Google
        driver.get("https://www.google.com")
        
        # Find the search box and enter the query
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results to load
        time.sleep(2)  # Adjust the sleep time if necessary
        
        # Wait for results to load
        time.sleep(2)  # Adjust the sleep time if necessary

        # Find the first result link and click it
        first_link = driver.find_element(By.CSS_SELECTOR, 'h3')
        first_link.click()
        
        # Locate the download link for .txt or .csv file
        # Adjust the CSS selector based on the actual page structure
        download_links = driver.find_elements(By.CSS_SELECTOR, 'a[href$=".txt"], a[href$=".csv"]')
        
        if download_links:
            download_link = download_links[0]  # Take the first available link
            download_link.click()
            print("Download triggered. Check the download directory.")
        else:
            print("No download link found.")
        
        # Wait to ensure the download starts
        time.sleep(5)  # Adjust time as needed for file download to start
        

    finally:
        # Close the WebDriver
        driver.quit()



