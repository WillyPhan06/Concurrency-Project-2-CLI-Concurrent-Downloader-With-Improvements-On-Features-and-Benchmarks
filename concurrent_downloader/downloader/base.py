from abc import ABC, abstractmethod

class BaseDownloader(ABC):
    def __init__(self, urls, output_dir):
        self.urls = urls
        self.output_dir = output_dir

    @abstractmethod
    def download(self):
        pass
