
import os
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from . import utils
from . import history_handler

class StationHandler(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_extension(os.path.abspath("./.local_db/youtube_extension.zip"))
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.queue = []
        self.currently_playing = ""
        
        thread = threading.Thread(target=self.video_thread)
        thread.start()
        
    def video_thread(self):
        # play silence to get past cookie prompt
        self.driver.get('https://www.youtube.com/watch?v=g4mHPeMGTJM')
        cookie_button_xpath = "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"
        # cookie_button_xpath = "//button[@aria-label='Reject the use of cookies and other data for the purposes described']"
        cookie = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, cookie_button_xpath)))
        cookie = self.driver.find_element_by_xpath(cookie_button_xpath)
        cookie.click()
        
        while True:
            if not self.video_is_playing() and len(self.queue) > 0:
                self.play_next_in_queue()
            time.sleep(1)
    
    def add_to_queue(self, url):
        self.queue.append(
            {
                "url": url, 
                "title": utils.get_video_title(url)
            }
        )
        
    def remove_from_queue(self, index):
        self.queue.pop(index)
        
    def play_next_in_queue(self):
        queue_data = self.queue[0]
        print(f"Playing queued video: {queue_data.get('title')}")
        del self.queue[0]
        self.play_youtube_video(queue_data.get("url"), queue_data.get("title"))

    def play_youtube_video(self, url, title=None):
        if title is None:
            title = utils.get_video_title(url)
        self.currently_playing = title
        self.driver.get(url)
        history_handler.INSTANCE.add_to_history(url, title)
    
    def get_current_video_title(self):
        return self.driver.execute_script("return document.title").replace(" - YouTube", "")
    
    def video_is_playing(self):
        if self.get_current_video_title() != self.currently_playing:
            return False
        return self.driver.execute_script("return document.getElementById('movie_player').getPlayerState()") == 1


class MockStationHandler():
    queue = [
        {
        "url": "https://www.youtube.com/watch?v=v-n1vGeVIXo",
        "title": "Mock Video Name"
        }
    ]
    
    def get_current_video_title(self):
        return "Mock Title"
    
    def add_to_queue(self, url):
        video_title = utils.get_video_title(url)
        self.queue.append({"url": url, "title": video_title})
        # history_handler.INSTANCE.add_to_history(url, video_title)
    
    def remove_from_queue(self, index):
        print(f"popping index: {index}")
        self.queue.pop(index)

        
INSTANCE = StationHandler()
# INSTANCE = MockStationHandler()
