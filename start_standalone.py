import os
import time
import json
import urllib
import socketserver
import http.server
import threading
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

os.makedirs("./.local_db", exist_ok=True)


class HistoryHandler(object):
    def __init__(self):
        self.db_path = "./.local_db/history_db.json"
    
    def add_to_history(self, url, title):
        history = self.get_history()
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        with open(self.db_path, "w") as fp:
            history.insert(0, 
                {
                "url": url,
                "title": title,
                "added": current_time
                }
            )
            json.dump(history, fp, indent=2)
    
    def get_history(self):
        history_data = []
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as fp:
                history_data = json.load(fp)
        return history_data



URL_TITLE_CACHE = {}
def get_video_title(url):
    if URL_TITLE_CACHE.get(url):
        return URL_TITLE_CACHE.get(url)
    
    import requests
    from bs4 import BeautifulSoup
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    
    video_title = ""
    titles = soup.find_all(name="title")
    if titles:
        video_title = titles[0].text.replace(" - YouTube", "")
        URL_TITLE_CACHE[url] = video_title
    
    return video_title


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
                "title": get_video_title(url)
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
            title = get_video_title(url)
        self.currently_playing = title
        self.driver.get(url)
        HISTORY_HANDLER.add_to_history(url, title)
    
    def get_current_video_title(self):
        return self.driver.execute_script("return document.title").replace(" - YouTube", "")
    
    def video_is_playing(self):
        if self.get_current_video_title() != self.currently_playing:
            return False
        return self.driver.execute_script("return document.getElementById('movie_player').getPlayerState()") == 1


def get_sanitized_url(url):
    video_url = urllib.parse.unquote(url)
    video_url = video_url.split("&")[0] # strip extra additions
    return video_url


def is_safe_youtube_url(url):
    video_url = get_sanitized_url(url)
    
    validated_url = video_url.lower().replace("https://", "").replace("www.", "")
    is_safe_url = validated_url.startswith("youtube.com")
    if is_safe_url:
        return True
    
    print(f"Failed url validation: {validated_url}")
    return False


class SoundStationHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if "current-video-title" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(STATION_HANDLER.get_current_video_title()).encode())
            return
        
        if "queue-list" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(STATION_HANDLER.queue).encode())
            return       
            
        if "history-list" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(HISTORY_HANDLER.get_history()).encode())
            return
        
        if "add-queue" in self.path:
            video_url_raw = self.path.split("target_url=")[-1]
            
            if is_safe_youtube_url(video_url_raw):
                safe_url = get_sanitized_url(video_url_raw)
                STATION_HANDLER.add_to_queue(safe_url)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'all good'}).encode())
            return
                
        if "remove-from-queue" in self.path:
            index = self.path.split("queue_index=")[-1]
            STATION_HANDLER.remove_from_queue(int(index))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'all good'}).encode())
            return
        
        if "play-video" in self.path:
            video_url_raw = self.path.split("target_url=")[-1]
            
            if is_safe_youtube_url(video_url_raw):
                safe_url = get_sanitized_url(video_url_raw)
                STATION_HANDLER.play_youtube_video(safe_url)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'all good'}).encode())
            return
        
        return super().do_GET()


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
        video_title = get_video_title(url)
        self.queue.append({"url": url, "title": video_title})
        HISTORY_HANDLER.add_to_history(url, video_title)
    
    def remove_from_queue(self, index):
        print(f"popping index: {index}")
        self.queue.pop(index)


HISTORY_HANDLER = HistoryHandler()
STATION_HANDLER = StationHandler()
# STATION_HANDLER = MockStationHandler()
# HISTORY_HANDLER.db_path = "./history_mock_db.json"


PORT = 8765
with socketserver.TCPServer(("", PORT), SoundStationHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

