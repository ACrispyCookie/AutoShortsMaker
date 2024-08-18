from praw.models import Redditor

from content.types.reddit_ask.wrappers.RedditContent import RedditContent


class RedditPost(RedditContent):

    def __init__(self, post_id: int, title: str, author: Redditor, url: str, screenshot_path: str, tts_path: str):
        super().__init__(post_id, title, author, url, screenshot_path, tts_path, "post")
