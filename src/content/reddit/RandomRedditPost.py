import random

import praw


class RandomDailyRedditPost:

    def __init__(self, credentials, subreddit, top_limit=10, exclude_nsfw=True, exclude_posts=None):
        if exclude_posts is None:
            exclude_posts = []
        self.credentials = credentials
        self.subreddit = subreddit
        self.limit = top_limit
        self.post = None
        self.exclude_nsfw = exclude_nsfw
        self.exclude_posts = exclude_posts

    def get(self):
        reddit = self.getReddit()
        top_posts = list(reddit.subreddit(self.subreddit).top(time_filter="day", limit=self.limit))

        random_index = random.randint(0, self.limit)
        while ((top_posts[random_index].over_18 and self.exclude_posts)
               or top_posts[random_index].id in self.exclude_posts):
            random_index = random.randint(0, self.limit)

        return top_posts[random_index]

    def getReddit(self):
        return praw.Reddit(
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            user_agent=self.credentials["user_agent"]
        )
