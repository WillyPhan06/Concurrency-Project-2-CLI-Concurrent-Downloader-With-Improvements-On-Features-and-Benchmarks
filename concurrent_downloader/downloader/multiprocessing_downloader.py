import time
import os
from concurrent.futures import ProcessPoolExecutor
import requests
from tqdm import tqdm
from .base import BaseDownloader


class Multiprocessing_Downloader(BaseDownloader):
    def __init__(self, urls, output_dir):
        super().__init__(urls, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        self.file_name_counter = 1

    def download_file_each_url(self, url):
        try:
            response = requests.get(url)
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
            print(f"✅SUCCEEDED✅ {url}")
        except Exception as e:
            print(f"❌FAILED❌ {url}: {e}")


    def download(self):
        start = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(self.download_file_each_url, self.urls)
        end = time.time() - start
        print(f"🚀MULTIPROCESSING DONE IN TOTAL OF {end:.2f} SECONDS!🚀")

