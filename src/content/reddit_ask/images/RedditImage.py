from abc import ABC, abstractmethod


class RedditImage(ABC):

    def __init__(self, reddit_content):
        self.content = reddit_content

    @abstractmethod
    def create(self):
        raise NotImplementedError
