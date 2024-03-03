import socketserver
import sound_station.http_handler

import os
if not os.path.exists("./.local_db"):
    os.makedirs("./.local_db")
    print("missing youtube_extension.zip file in local_db")

PORT = 8765
with socketserver.TCPServer(("", PORT), sound_station.http_handler.SoundStationHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
