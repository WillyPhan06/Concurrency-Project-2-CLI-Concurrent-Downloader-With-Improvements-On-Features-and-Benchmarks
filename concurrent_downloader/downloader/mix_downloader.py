from .threading_downloader import Threading_Downloader
from .multiprocessing_downloader import Multiprocessing_Downloader
from .asyncio_downloader import Asyncio_Downloader
from .base import BaseDownloader
from concurrent.futures import ThreadPoolExecutor
import time

class Mix_Downloader(BaseDownloader):
    def __init__(self, urls, output_dir):
        super().__init__(urls, output_dir)
        self.len_urls = len(self.urls)
        self.downloader_1 = Multiprocessing_Downloader(urls[:(self.len_urls//3)], output_dir)
        self.downloader_2 = Threading_Downloader(urls[(self.len_urls//3):(self.len_urls//3*2)], output_dir)
        self.downloader_3 = Asyncio_Downloader(urls[(self.len_urls//3*2):], output_dir)

    def download(self):
        start = time.time()
        with ThreadPoolExecutor(max_workers=3) as executor:
            print("🚀 Starting Multiprocessing Download First Third URLS 🚀")
            executor.submit(self.downloader_1.download)
            print("🚀 Starting Threading Download Second Third URLS 🚀")
            executor.submit(self.downloader_2.download)
            print("🚀 Starting Asyncio Download Last Third URLS 🚀")
            executor.submit(self.downloader_3.download)
        
        end = time.time() - start
        print(f"🚀 MIX DONE IN TOTAL OF {end:.2f} SECONDS! 🚀")