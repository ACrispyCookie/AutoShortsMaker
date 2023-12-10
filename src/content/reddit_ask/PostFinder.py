import praw

from src.content.reddit_ask.tts.SimpleTTS import SimpleTTS
from src.content.reddit_ask.wrappers.RedditComment import RedditComment
from src.content.reddit_ask.wrappers.RedditPost import RedditPost


class PostFinder:

    def __init__(self, credentials, subreddit, top_limit=10, exclude_nsfw=True, exclude_posts=None):
        if exclude_posts is None:
            exclude_posts = []
        self.credentials = credentials
        self.subreddit = subreddit
        self.limit = top_limit
        self.post = None
        self.exclude_nsfw = exclude_nsfw
        self.exclude_posts = exclude_posts

    def get(self, max_duration, max_comment_length, tts_type, images_path, tts_path):
        reddit = self.getReddit()
        top_posts = list(reddit.subreddit(self.subreddit).top(time_filter="day", limit=self.limit))

        index = 0
        while ((top_posts[index].over_18 and self.exclude_posts)
               or top_posts[index].id in self.exclude_posts):
            index += 1

        post = top_posts[index]
        wrapped_post = RedditPost(post.id, post.title, post.author, post.url, images_path, tts_path)
        wrapped_comments = []
        for comment in post.comments[:-1]:
            if not isCommentValid(comment, max_comment_length):
                continue
            wrapped_comments.append(RedditComment(comment.id, comment.body, comment.author,
                                                  post.url, images_path, tts_path))
        used_comments, duration = getUsedComments(wrapped_post, wrapped_comments, max_duration,
                                                  tts_type)
        return wrapped_post, used_comments, duration

    def getReddit(self):
        return praw.Reddit(
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            user_agent=self.credentials["user_agent"]
        )


def getUsedComments(post, comments, max_duration, tts_type):
    currentDuration = 0
    usedComments = []

    print("Creating text-to-speech files...")
    duration = SimpleTTS(post).create().getDuration() if tts_type == "simple" else 0  # TODO fix ai tts
    post.setDuration(duration)
    currentDuration += post.tts_duration

    for comment in comments:
        duration = SimpleTTS(comment).create().getDuration() if tts_type == "simple" else 0  # TODO fix ai tts
        if currentDuration + duration > max_duration:
            break
        comment.setDuration(duration)
        currentDuration += duration
        usedComments.append(comment)

    return usedComments, currentDuration


def isCommentValid(comment, maxCommentLength):
    if comment.body == '[deleted]' or comment.body == '[removed]' or comment.body == '':
        return False
    if len(comment.body) > maxCommentLength:
        return False
    return True
