from src.content.Content import Content
import src.content.reddit_ask.background.BackgroundVideoManager as BVM
from src.content.reddit_ask.PostFinder import PostFinder
from src.content.reddit_ask.images.RedditTemplate import RedditTemplate
from src.content.reddit_ask.images.RedditScreenshot import RedditScreenshot
from src.content.reddit_ask.tts.SimpleTTS import SimpleTTS
from src.content.reddit_ask.video.RedditVideoComposer import RedditVideoComposer


class RedditAskContent(Content):

    def __init__(self, config, data):
        super().__init__("REDDIT_ASK", config, data)
        self.post = None
        self.comments = []
        self.duration = 0

        self.subreddit = self.config["settings"]["subreddit"]
        self.max_duration = self.config["settings"]["max_duration"]
        self.max_comment_length = self.config["settings"]["max_comment_length"]
        self.image_mode = self.config["settings"]["image_mode"]
        self.tts_mode = self.config["settings"]["tts_mode"]

    def create(self):
        if self.config["download_background"]["enabled"]:
            print("Downloading background videos...")
            BVM.downloadBackgroundVideos(self.config["download_background"]["url"],
                                         self.config["download_background"]["playlist"],
                                         self.dirs["background_videos"])

        print("Resizing background videos...")
        BVM.cropBackgroundVideos(self.dirs["background_videos"])

        print("Getting a random post...")
        (self.post,
         self.comments,
         self.duration) = (
            PostFinder(credentials=self.getCredentials(), subreddit=self.subreddit, exclude_posts=self.data["posts"])
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

    def getCredentials(self):
        return {"client_id": self.config["client_id"], "client_secret": self.config["client_secret"],
                "user_agent": self.config["user_agent"]}
