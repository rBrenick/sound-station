import json
import http.server
from . import history_handler
from . import station_handler
from . import utils

class SoundStationHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if "/current-video-title" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(station_handler.INSTANCE.get_current_video_title()).encode())
            return
        
        elif "/queue-list" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(station_handler.INSTANCE.queue).encode())
            return
            
        elif "/history-list" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(history_handler.INSTANCE.get_history()).encode())
            return
        
        elif "/add-to-queue" in self.path:
            video_url_raw = self.path.split("target_url=")[-1]
            
            if utils.is_safe_youtube_url(video_url_raw):
                safe_url = utils.get_sanitized_url(video_url_raw)
                station_handler.INSTANCE.add_to_queue(safe_url)

            self.send_response(200)
            self.end_headers()
            return
        
        elif "/remove-from-queue" in self.path:
            index = self.path.split("queue_index=")[-1]
            station_handler.INSTANCE.remove_from_queue(int(index))
            self.send_response(200)
            self.end_headers()
            return
        
        elif "/play-video-from-url" in self.path:
            video_url_raw = self.path.split("target_url=")[-1]
            
            if utils.is_safe_youtube_url(video_url_raw):
                safe_url = utils.get_sanitized_url(video_url_raw)
                station_handler.INSTANCE.play_video_from_url(safe_url)

            self.send_response(200)
            self.end_headers()
            return
                
        elif "/pause-video" in self.path:
            station_handler.INSTANCE.pause_video()
            self.send_response(200)
            self.end_headers()
            return
            
        elif "/play-video" in self.path:
            station_handler.INSTANCE.play_video()
            self.send_response(200)
            self.end_headers()
            return
        
        elif "/get-volume" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(station_handler.INSTANCE.get_volume()).encode())
            return
        
        elif "/set-volume" in self.path:
            volume_value = self.path.split("value=")[-1]
            station_handler.INSTANCE.set_volume(int(volume_value))
            self.send_response(200)
            self.end_headers()
            return
        
        return super().do_GET()
