import os
from datetime import datetime
from threading import Lock

class Logger:
    def __init__(self, output_dir, method):
        self.output_dir = output_dir
        self.lock = Lock()
        self.method = method
        
        with open(self.output_dir, "a") as log:
            log.write(f"{self.method.upper()} LOG HISTORY\n")

    def log(self, url, status, message=""):
        time = datetime.now().strftime("[%d/%m/%Y - %H:%M:%S]")
        log_line = f"{time} {status} {url} {message}\n"
        try:
            with self.lock:
                with open(self.output_dir, "a") as url_log:
                    url_log.write(log_line)
        except Exception as e:
            print(f"❌ERROR HAPPENED WHILE WRITING LOG: {e}❌")
