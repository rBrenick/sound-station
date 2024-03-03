import os
import json
from datetime import datetime

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


INSTANCE = HistoryHandler()
# INSTANCE.db_path = "./history_mock_db.json"


