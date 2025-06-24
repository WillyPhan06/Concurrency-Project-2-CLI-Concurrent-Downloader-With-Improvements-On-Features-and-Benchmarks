import asyncio
import aiohttp
import time
import os
from tqdm.asyncio import tqdm
from .base import BaseDownloader
from .logger import Logger

class Asyncio_Downloader(BaseDownloader):
    def __init__(self, urls, output_dir):
        super().__init__(urls, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        self.logger = Logger(os.path.join("logs", "log.txt"), "ASYNCIO")
        self.success_count = 0
        self.fail_count = 0
        self.lock = asyncio.Lock()
        self.file_name_counter = 1

        
    async def download_file_each_url(self, url, session):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length",0))
                save_file = os.path.join(self.output_dir, url.split("/")[-1])
                while os.path.exists(save_file):
                    save_file = os.path.join(self.output_dir, f"{url.split('/')[-1]}_{self.file_name_counter}")
                    self.file_name_counter += 1
                with open(save_file, "wb") as f, tqdm(desc=save_file, total=total, unit="B", unit_scale=True, unit_divisor=1024) as bar:
                    async for chunk in response.content.iter_chunked(1024):
                        f.write(chunk)
                        bar.update(len(chunk))
            async with self.lock:
                self.logger.log(url, "SUCCESS")
                self.success_count += 1
            print(f"✅SUCCEEDED✅ {url}")
        except Exception as e:
            async with self.lock:
                self.logger.log(url, "FAIL", e)
                self.fail_count += 1
            print(f"❌FAILED❌ {url}: {e}")

    async def run(self):
        connector = aiohttp.TCPConnector(limit=10)
        timeout = aiohttp.ClientTimeout(total=60)
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
        }
        try: 
            async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers) as session:
                await asyncio.gather(*(self.download_file_each_url(url, session) for url in self.urls))
        except Exception as e:
            print(f"❌ERROR HAPPENED WHILE CREATING SESSIONS AND GATHERING TASKS: {e}❌")


    def download(self):
        start = time.time()
        asyncio.run(self.run())
        end = time.time() - start
        print(f"🚀ASYNCIO DONE IN TOTAL OF {end:.2f} SECONDS!🚀")
        print(f"✅TOTAL SUCESS: {self.success_count}✅")
        print(f"❌TOTAL FAIL: {self.fail_count}❌")


