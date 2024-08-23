from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def play_youtube_video(video_query):
    # Set up Chrome WebDriver
    option = webdriver.ChromeOptions()

    option.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=option)
    
    try:
        # Open YouTube
        driver.get("https://www.youtube.com")
        
        # Find the search box, enter the video query, and hit Enter
        search_box = driver.find_element("name", "search_query")
        search_box.send_keys(video_query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the search results to load
        time.sleep(2)  # Adjust as necessary
        
        # Find the first video link and click it
        video = driver.find_element("id", "video-title")
        video.click()
        
        # Wait for the video to load and start playing
        time.sleep(5)  # Adjust as necessary for your network speed
        
    finally:
        # Optionally, keep the browser open or close it
        # driver.quit()
        pass

# Example usage

