from src.content.reddit.RedditContent import RedditContent


class RedditComment(RedditContent):

    def __init__(self, comment_id, body):
        super().__init__(comment_id, body, "comment")
