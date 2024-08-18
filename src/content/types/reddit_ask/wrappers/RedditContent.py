from praw.models import Redditor


class RedditContent:

    def __init__(self, post_id: int, title: str, author: Redditor, url: str, images_path: str, tts_path: str, content_type: str):
        self.id: int = post_id
        self.body: str = title
        self.author: str = author.name
        self.url: str = url
        self.type: str = content_type
        self.image: str = images_path + content_type + "-" + str(post_id) + ".png"
        self.tts: str = tts_path + content_type + "-" + str(post_id) + ".mp3"
        self.tts_duration: int = 0

    def set_duration(self, duration):
        self.tts_duration: int = duration
