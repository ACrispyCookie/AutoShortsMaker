class RedditContent:

    def __init__(self, post_id, title, content_type):
        self.id = post_id
        self.body = title
        self.type = content_type
        self.screenshot = "screenshots/reddit_ask/" + content_type + "-" + post_id + ".png"
        self.tts = "tts/reddit_ask/" + content_type + "-" + post_id + ".mp3"
        self.tts_duration = 0

    def setDuration(self, duration):
        self.tts_duration = duration
