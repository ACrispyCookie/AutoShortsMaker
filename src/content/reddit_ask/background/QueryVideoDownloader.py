from src.content.reddit_ask.background.VideoDownloader import VideoDownloader


class QueryVideoDownloader(VideoDownloader):

    def __init__(self, folder, name, url):
        super().__init__(folder, name)
        self.url = url

    def download(self):
        print("Downloading video from url: " + self.url)
