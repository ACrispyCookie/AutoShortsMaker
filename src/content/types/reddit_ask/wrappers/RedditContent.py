from praw.models import Redditor


class RedditContent:

    def __init__(self, post_id: int, title: str, author: Redditor, url: str, images_path: str, tts_path: str, content_type: str):
        self.id = post_id
        self.body = title
        self.author = author.name
        self.url = url
        self.type = content_type
        self.image = images_path + content_type + "-" + str(post_id) + ".png"
        self.tts = tts_path + content_type + "-" + str(post_id) + ".mp3"
        self.tts_duration = 0

    def set_duration(self, duration):
        self.tts_duration = duration
