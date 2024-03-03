import urllib

import requests
from bs4 import BeautifulSoup

URL_TITLE_CACHE = {}
def get_video_title(url):
    if URL_TITLE_CACHE.get(url):
        return URL_TITLE_CACHE.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    
    video_title = ""
    titles = soup.find_all(name="title")
    if titles:
        video_title = titles[0].text.replace(" - YouTube", "")
        URL_TITLE_CACHE[url] = video_title
    
    return video_title

    
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
    
 