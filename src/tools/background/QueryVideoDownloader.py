from tools.background.VideoDownloader import VideoDownloader


class QueryVideoDownloader(VideoDownloader):

    def __init__(self, folder: str, name: str, url: str):
        super().__init__(folder, name)
        self.url: str = url

    def download(self):
        print("Downloading video from url: " + self.url)
