from src.content.reddit_ask.wrappers.RedditContent import RedditContent


class RedditPost(RedditContent):

    def __init__(self, post_id, title, author, url, screenshot_path, tts_path):
        super().__init__(post_id, title, author, url, screenshot_path, tts_path, "post")
