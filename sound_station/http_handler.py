import json
import http.server
from . import history_handler
from . import station_handler
from . import utils

class SoundStationHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if "current-video-title" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(station_handler.INSTANCE.get_current_video_title()).encode())
            return
        
        if "queue-list" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(station_handler.INSTANCE.queue).encode())
            return       
            
        if "history-list" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(history_handler.INSTANCE.get_history()).encode())
            return
        
        if "add-queue" in self.path:
            video_url_raw = self.path.split("target_url=")[-1]
            
            if utils.is_safe_youtube_url(video_url_raw):
                safe_url = utils.get_sanitized_url(video_url_raw)
                station_handler.INSTANCE.add_to_queue(safe_url)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'all good'}).encode())
            return
                
        if "remove-from-queue" in self.path:
            index = self.path.split("queue_index=")[-1]
            station_handler.INSTANCE.remove_from_queue(int(index))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'all good'}).encode())
            return
        
        if "play-video" in self.path:
            video_url_raw = self.path.split("target_url=")[-1]
            
            if utils.is_safe_youtube_url(video_url_raw):
                safe_url = utils.get_sanitized_url(video_url_raw)
                station_handler.INSTANCE.play_youtube_video(safe_url)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'all good'}).encode())
            return
        
        return super().do_GET()
