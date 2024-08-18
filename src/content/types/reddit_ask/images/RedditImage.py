from abc import ABC, abstractmethod

from content.types.reddit_ask.wrappers.RedditContent import RedditContent


class RedditImage(ABC):

    def __init__(self, reddit_content: RedditContent):
        self.content: RedditContent = reddit_content

    @abstractmethod
    def create(self):
        raise NotImplementedError
