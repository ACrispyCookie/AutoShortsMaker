from content.background.VideoDownloader import VideoDownloader
import pytube


class UrlVideoDownloader(VideoDownloader):

    def __init__(self, url, playlist, folder, name):
        super().__init__(folder, name)
        self.url = url
        self.playlist = playlist

    def download(self):  # TODO fix this
        yt_video = pytube.YouTube(self.url)
        stream_query = yt_video.streams.filter(type="video", progressive=False).order_by('resolution').desc()
        print(stream_query.first())
        stream = stream_query.first() if stream_query.first().resolution == "1080p" else stream_query.filter(
            res="1080p").first()
        stream.download(self.folder, self.name, None, False)

