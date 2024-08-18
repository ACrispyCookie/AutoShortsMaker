from abc import ABC, abstractmethod


class VideoDownloader(ABC):

    def __init__(self, folder, name):
        self.folder = folder
        self.name = name

    @abstractmethod
    def download(self):
        raise NotImplementedError("Subclass must implement abstract method")
