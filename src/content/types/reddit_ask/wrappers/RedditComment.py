from praw.models import Redditor

from content.types.reddit_ask.wrappers.RedditContent import RedditContent


class RedditComment(RedditContent):

    def __init__(self, comment_id: int, body: str, author: Redditor, url: str, images_path: str, tts_path: str):
        super().__init__(comment_id, body, author, url, images_path, tts_path, "comment")
