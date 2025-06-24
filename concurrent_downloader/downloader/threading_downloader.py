import time
from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm import tqdm
from .base import BaseDownloader
from .logger import Logger
import os
from threading import Lock


class Threading_Downloader(BaseDownloader):
    def __init__(self, urls, output_dir):
        super().__init__(urls, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        self.logger = Logger(os.path.join("logs", "log.txt"), "THREADING")
        self.success_count = 0
        self.fail_count = 0
        self.lock = Lock()
        self.file_name_counter = 1

    def download_file_each_url(self, url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total = int(response.headers.get("content-length",0))
            save_file = os.path.join(self.output_dir, url.split("/")[-1])
            while os.path.exists(save_file):
                save_file = os.path.join(self.output_dir, f"{url.split('/')[-1]}_{self.file_name_counter}")
                self.file_name_counter += 1
            with open(save_file, "wb") as f, tqdm(desc=save_file, total=total, unit="B", unit_scale=True, unit_divisor=1024) as bar:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                    bar.update(len(chunk))
            with self.lock:
                self.success_count += 1
                self.logger.log(url, "SUCCESS")
            print(f"✅SUCCEEDED✅ {url}") 
        except Exception as e:
            with self.lock:
                self.fail_count += 1
                self.logger.log(url, "FAIL", e)
            print(f"❌FAILED❌ {url}: {e}")
            

    def download(self):
        start = time.time()
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(self.download_file_each_url, self.urls)
        end = time.time() - start
        print(f"🚀THREADING DONE IN TOTAL OF {end:.2f} SECONDS!🚀")
        print(f"✅TOTAL SUCESS: {self.success_count}✅")
        print(f"❌TOTAL FAIL: {self.fail_count}❌")
        
