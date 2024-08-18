from pytube import YouTube, StreamQuery, Stream

from content.background.VideoDownloader import VideoDownloader
import pytube


class UrlVideoDownloader(VideoDownloader):

    def __init__(self, url: str, playlist: bool, folder: str, name: str):
        super().__init__(folder, name)
        self.url: str = url
        self.playlist: bool = playlist

    def download(self):  # TODO fix this
        yt_video: YouTube = pytube.YouTube(self.url)
        stream_query: StreamQuery = yt_video.streams.filter(type="video", progressive=False).order_by('resolution').desc()
        print(stream_query.first())
        stream: Stream = stream_query.first() if stream_query.first().resolution == "1080p" else stream_query.filter(
            res="1080p").first()
        stream.download(self.folder, self.name, None, False)

