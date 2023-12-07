import os
from src.content.Content import Content
from src.background.BackgroundUrlVideo import BackgroundUrlVideo
from src.background.BackgroundVideo import cropBackgroundVideo
from src.content.reddit.RandomRedditPost import RandomDailyRedditPost
from src.video.RedditVideoComposer import RedditVideoComposer


class RedditAskContent(Content):

    def __init__(self, config, data):
        super().__init__("REDDIT_ASK", config, data)
        self.post = None
        self.comments = []
        self.composer = None

    def create(self):
        if self.config["download_background"]["enabled"]:
            print("Downloading background videos...")
            self.downloadBackgroundVideos()

        print("Resizing background videos...")
        cropBackgroundVideos()

        print("Getting a random post...")
        self.post = self.getRandomPost()
        self.comments = self.post.comments
        self.data["posts"].append(self.post.id)
        self.saveData()

        self.composer = RedditVideoComposer(self.post, self.comments)
        print("Creating text to speech audio...")
        self.composer.createTextToSpeech()

        print("Screenshotting post...")
        self.composer.screenshotPost()

        print("Composing video...")
        self.composer.composeVideo()

    def downloadBackgroundVideos(self, folder="background_videos/reddit_ask"):
        url = self.config["download_background"]["url"]
        playlist = self.config["download_background"]["playlist"]

        BackgroundUrlVideo(url=url, playlist=playlist,
                           folder=folder, name=getFirstVideoName()).download()

    def getRandomPost(self):
        return RandomDailyRedditPost(
            {"client_id": self.config["client_id"], "client_secret": self.config["client_secret"],
             "user_agent": self.config["user_agent"]}, self.config["subreddit"],
            exclude_posts=self.data["posts"]).get()


def cropBackgroundVideos(folder="background_videos/reddit_ask"):
    for file in os.listdir(folder):
        if file.endswith(".webm"):
            cropBackgroundVideo(folder + "/" + file,
                                folder + "/" + file.removesuffix(".webm") + "_final.webm")
            if os.path.exists(folder + "/" + file.removesuffix(".webm") + "_final.webm"):
                os.rename(folder + "/" + file.removesuffix(".webm") + "_final.webm", folder + "/" + file)


def getFirstVideoName(folder="background_videos/reddit_ask"):
    name = "video_0"
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        name = name.removesuffix("0") + str(len(os.listdir(folder)))
    return name
