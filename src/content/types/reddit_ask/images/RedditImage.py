from abc import ABC, abstractmethod
from enum import Enum

from content.types.reddit_ask.wrappers.RedditContent import RedditContent

class RedditImageMode(Enum):
    SCREENSHOT = 1
    TEMPLATE = 2


class RedditImage(ABC):

    def __init__(self, reddit_content: RedditContent):
        self.content: RedditContent = reddit_content

    @abstractmethod
    def create(self):
        raise NotImplementedError
