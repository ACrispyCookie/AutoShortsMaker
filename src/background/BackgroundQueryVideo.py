from src.background.BackgroundVideo import BackgroundVideo


class BackgroundQueryVideo(BackgroundVideo):

    def __init__(self, folder, name, url):
        super().__init__(folder, name)
        self.url = url

    def download(self):
        print("Downloading video from url: " + self.url)
