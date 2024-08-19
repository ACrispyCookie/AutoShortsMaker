from abc import ABC, abstractmethod


class VideoDownloader(ABC):

    def __init__(self, folder: str, name: str):
        self.folder: str = folder
        self.name: str = name

    @abstractmethod
    def download(self):
        raise NotImplementedError("Subclass must implement abstract method")
