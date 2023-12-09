class RedditContent:

    def __init__(self, post_id, title, author, url, images_path, tts_path, content_type):
        self.id = post_id
        self.body = title
        self.author = author.name
        self.url = url
        self.type = content_type
        self.image = images_path + content_type + "-" + post_id + ".png"
        self.tts = tts_path + content_type + "-" + post_id + ".mp3"
        self.tts_duration = 0

    def setDuration(self, duration):
        self.tts_duration = duration
