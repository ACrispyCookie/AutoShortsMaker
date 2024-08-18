from typing import Dict, Any

from content.Content import ContentType
from src.content.Content import Content
import content.background.BackgroundVideoManager as Bvm
from content.types.reddit_ask.PostFinder import PostFinder
from content.types.reddit_ask.images.RedditTemplate import RedditTemplate
from content.types.reddit_ask.images.RedditScreenshot import RedditScreenshot
from content.types.reddit_ask.video.RedditVideoComposer import RedditVideoComposer


class RedditAskContent(Content):

    def __init__(self, config: Dict[str, Any], data: Dict[str, Any], secrets: Dict[str, Any]):
        super().__init__(ContentType.REDDIT_ASK, config, data, secrets)
        self.post = None
        self.comments = []
        self.duration = 0

        self.subreddit = self.config["settings"]["subreddit"]
        self.max_duration = self.config["settings"]["max_duration"]
        self.max_comment_length = self.config["settings"]["max_comment_length"]
        self.image_mode = self.config["settings"]["image_mode"]
        self.tts_mode = self.config["settings"]["tts_mode"]

    def create(self) -> None:
        if self.config["download_background"]["enabled"]:
            print("Downloading background videos...")
            Bvm.downloadBackgroundVideos(self.config["download_background"]["url"],
                                         self.config["download_background"]["playlist"],
                                         self.dirs["background_videos"])

        print("Resizing background videos...")
        Bvm.cropBackgroundVideos(self.dirs["background_videos"])

        print("Getting a random post...")
        (self.post,
         self.comments,
         self.duration) = (
            PostFinder(credentials=self.get_credentials(), subreddit=self.subreddit,
                       exclude_posts=(self.data["posts"] if "posts" in self.data.keys() else []))
            .get(self.max_duration, self.max_comment_length, self.tts_mode, self.dirs["images"], self.dirs["tts"]))

        if "posts" in self.data.keys():
            self.data["posts"].append(self.post.id)
        else:
            self.data["posts"] = [self.post.id]

        self.save_data()

        print("Screenshotting post...")
        if self.image_mode == "screenshot":
            RedditScreenshot(self.post).create()
            for comment in self.comments:
                RedditScreenshot(comment).create()
        else:
            RedditTemplate(self.post).create()
            for comment in self.comments:
                RedditTemplate(comment).create()

        print("Composing video...")
        (RedditVideoComposer(self.post, self.comments, self.duration,
                             self.dirs["background_videos"], self.dirs["final_videos"])
         .composeVideo(self.config["settings"]["video"]["bitrate"], self.config["settings"]["video"]["threads"]))

    def get_credentials(self) -> Dict[str, str]:
        return {"client_id": self.secrets["reddit_client_id"], "client_secret": self.secrets["reddit_client_secret"],
                "user_agent": self.secrets["reddit_user_agent"]}
