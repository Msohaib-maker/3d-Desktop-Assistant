from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_latest_google_news(query):
    # Set up Chrome WebDriver
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=option)
    
    try:
        # Open Google News
        driver.get("https://news.google.com")
        
        # Wait for the page to load
        time.sleep(2)
        
        # Find the search box, enter the query, and hit Enter
        search_box = driver.find_element("xpath", '//input[@placeholder="Search"]')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results to load
        time.sleep(2)
        
        # Find the headlines of the news articles
        headlines = driver.find_elements("xpath", '//article//h3')
        
        # Extract and print the text of the first few headlines
        news_list = [headline.text for headline in headlines[:5]]  # Get the first 5 headlines
        
        return news_list
    
    finally:
        pass
        # Optionally, close the browser
        # driver.quit()

# Example usage

