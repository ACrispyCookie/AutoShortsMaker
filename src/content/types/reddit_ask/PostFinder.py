from typing import Dict, List, Tuple

import praw
from praw import Reddit
from praw.models import Submission, Comment, MoreComments

from tools.tts.ElevenLabsTTS import ElevenLabsTTS
from tools.tts.TextToSpeech import TTSMode, TextToSpeech
from tools.tts.SimpleTTS import SimpleTTS
from content.types.reddit_ask.wrappers.RedditComment import RedditComment
from content.types.reddit_ask.wrappers.RedditPost import RedditPost


class PostFinder:

    def __init__(self, credentials: Dict[str, str], subreddit: str, top_limit:int = 10, exclude_nsfw:bool = True, exclude_posts:List[str] = None, voice_to_use: str = ""):
        if exclude_posts is None:
            exclude_posts = []
        self.voice_to_use = voice_to_use
        self.credentials = credentials
        self.subreddit = subreddit
        self.limit = top_limit
        self.post = None
        self.exclude_nsfw = exclude_nsfw
        self.exclude_posts = exclude_posts

    def get(self, max_duration: int, max_comment_length: int, tts_type: TTSMode, images_path: str, tts_path: str) -> Tuple[RedditPost, List[RedditComment], int]:
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
                                                    tts_type, self.voice_to_use)
        return wrapped_post, used_comments, duration

    def get_reddit(self) -> Reddit:
        return praw.Reddit(
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            user_agent=self.credentials["user_agent"]
        )


def get_used_comments(post: RedditPost, comments: List[RedditComment], max_duration: int, tts_type: TTSMode, voice_to_use: str) -> Tuple[List[RedditComment], int]:
    current_duration: int = 0
    used_comments: List[RedditComment] = []

    print("Creating text-to-speech files...")
    tts: TextToSpeech = ElevenLabsTTS(post.body, post.tts, voice_to_use) if tts_type == TTSMode.ELEVEN_LABS else SimpleTTS(post.body, post.tts)
    duration: int = tts.create().get_duration()
    post.set_duration(duration)
    current_duration += post.tts_duration

    for comment in comments:
        tts = ElevenLabsTTS(comment.body, comment.tts, voice_to_use) if tts_type == TTSMode.ELEVEN_LABS else SimpleTTS(comment.body, comment.tts)
        duration = tts.create().get_duration()
        if current_duration + duration > max_duration:
            break
        comment.set_duration(duration)
        current_duration += duration
        used_comments.append(comment)

    return used_comments, current_duration


def is_comment_valid(comment: Comment | MoreComments, max_comment_length: int) -> bool:
    if type(comment) == MoreComments:
        return False
    if comment.author is None:
        return False
    if comment.body == '[deleted]' or comment.body == '[removed]' or comment.body == '':
        return False
    if len(comment.body) > max_comment_length:
        return False
    return True
