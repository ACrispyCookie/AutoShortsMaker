from src.content.reddit.RedditContent import RedditContent


class RedditPost(RedditContent):

    def __init__(self, post_id, title, url):
        super().__init__(post_id, title, "post")
        self.url = url
