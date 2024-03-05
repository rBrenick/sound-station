import os
import sys

if not os.path.exists("./.local_db"):
    sys.exit("missing ./local_db folder for youtube extension")

import socketserver
import sound_station.http_handler

PORT = 8765
with socketserver.TCPServer(("", PORT), sound_station.http_handler.SoundStationHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
