import array
from typing import Dict, List, Tuple

import praw
from praw import Reddit
from praw.models import Submission, Comment

from content.tts.TextToSpeech import TTSType, TextToSpeech
from src.content.tts.SimpleTTS import SimpleTTS
from content.types.reddit_ask.wrappers.RedditComment import RedditComment
from content.types.reddit_ask.wrappers.RedditPost import RedditPost


class PostFinder:

    def __init__(self, credentials: Dict[str, str], subreddit: str, top_limit:int = 10, exclude_nsfw:bool = True, exclude_posts:List[str] = None):
        if exclude_posts is None:
            exclude_posts = []
        self.credentials = credentials
        self.subreddit = subreddit
        self.limit = top_limit
        self.post = None
        self.exclude_nsfw = exclude_nsfw
        self.exclude_posts = exclude_posts

    def get(self, max_duration: int, max_comment_length: int, tts_type: TTSType, images_path: str, tts_path: str) -> Tuple[RedditPost, List[RedditComment], int]:
        reddit: Reddit = self.get_reddit()
        top_posts: List[Submission] = list(reddit.subreddit(self.subreddit).top(time_filter="day", limit=self.limit))

        index = 0
        while ((top_posts[index].over_18 and self.exclude_posts)
               or top_posts[index].id in self.exclude_posts):
            index += 1

        post: Submission = top_posts[index]
        wrapped_post: RedditPost = RedditPost(post.id, post.title, post.author, post.url, images_path, tts_path)
        wrapped_comments: List[RedditComment] = []
        for comment in post.comments[:-1]:
            if not is_comment_valid(comment, max_comment_length):
                continue
            wrapped_comments.append(RedditComment(comment.id, comment.body, comment.author,
                                                  post.url, images_path, tts_path))
        used_comments, duration = get_used_comments(wrapped_post, wrapped_comments, max_duration,
                                                    tts_type)
        return wrapped_post, used_comments, duration

    def get_reddit(self) -> Reddit:
        return praw.Reddit(
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            user_agent=self.credentials["user_agent"]
        )


def get_used_comments(post: RedditPost, comments: List[RedditComment], max_duration: int, tts_type: TTSType) -> Tuple[List[RedditComment], int]:
    current_duration: int = 0
    used_comments: List[RedditComment] = []

    print("Creating text-to-speech files...")
    tts: TextToSpeech = SimpleTTS(post.body, str(post.id)) if tts_type == TTSType.DEFAULT else SimpleTTS(post.body, str(post.id))
    duration: int = tts.create().get_duration()
    post.set_duration(duration)
    current_duration += post.tts_duration

    for comment in comments:
        tts = SimpleTTS(comment.body, str(comment.id)) if tts_type == TTSType.DEFAULT else SimpleTTS(comment.body, str(comment.id))
        duration = tts.create().get_duration()
        if current_duration + duration > max_duration:
            break
        comment.set_duration(duration)
        current_duration += duration
        used_comments.append(comment)

    return used_comments, current_duration


def is_comment_valid(comment: Comment, max_comment_length: int) -> bool:
    if comment.body == '[deleted]' or comment.body == '[removed]' or comment.body == '':
        return False
    if len(comment.body) > max_comment_length:
        return False
    return True
