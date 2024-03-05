
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
        
        chrome_options = webdriver.ChromeOptions()
        extension_path = os.path.abspath("./.local_db/youtube_extension.zip")
        if os.path.exists(extension_path):
            chrome_options.add_extension(extension_path)
        
        self.driver = webdriver.Chrome(options=chrome_options)

        self.queue = []
        
        self.starting_video_title = ""
        
        thread = threading.Thread(target=self.video_thread)
        thread.start()
        
    def video_thread(self):
        # play silence to get past cookie prompt
        self.driver.get('https://www.youtube.com/watch?v=g4mHPeMGTJM')
        cookie_button_xpath = "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"
        # cookie_button_xpath = "//button[@aria-label='Reject the use of cookies and other data for the purposes described']"
        cookie = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, cookie_button_xpath)))
        cookie = self.driver.find_element(By.XPATH, cookie_button_xpath)
        cookie.click()
        time.sleep(3)
        self.starting_video_title = self.get_current_video_title()
        self.pause_video()
        
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
        del self.queue[0]
        print(f"Playing queued video: {queue_data.get('title')}")
        self.play_video_from_url(queue_data.get("url"), queue_data.get("title"))

    def play_video_from_url(self, url, title=None):
        
        self.driver.get(url)
        
        if title is None:
            title = self.get_current_video_title()
        history_handler.INSTANCE.add_to_history(url, title)
    
    def pause_video(self):
        self.driver.execute_script("document.getElementById('movie_player').pauseVideo()")
        
    def play_video(self):
        self.driver.execute_script("document.getElementById('movie_player').playVideo()")
        
    def set_volume(self, value):
        self.driver.execute_script(f"document.getElementById('movie_player').setVolume({value})")

    def get_volume(self):
        return self.driver.execute_script("return document.getElementById('movie_player').getVolume()")

    def get_current_video_title(self):
        return self.driver.execute_script("return document.title").replace(" - YouTube", "")
    
    def video_is_playing(self):
        # if we're still on the starting "10-hour silence", we can say it's not playing any video
        if self.get_current_video_title() == self.starting_video_title:
            return False
        return self.driver.execute_script("return document.getElementById('movie_player').getPlayerState()") != 0


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

