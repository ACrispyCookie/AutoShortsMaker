from src.content.reddit_ask.wrappers.RedditContent import RedditContent


class RedditComment(RedditContent):

    def __init__(self, comment_id, body, author, url, images_path, tts_path):
        super().__init__(comment_id, body, author, url, images_path, tts_path, "comment")
