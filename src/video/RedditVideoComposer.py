import os
import random

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from src.screenshot.RedditScreenshot import RedditScreenshot
from src.tts.TextToSpeech import TextToSpeech


class RedditVideoComposer:

    def __init__(self, post, comments, maxDuration=45):
        self.post = post
        self.comments = comments
        self.maxDuration = maxDuration
        self.marginSize = 80
        self.postDuration = 0
        self.commentsUsed = []
        self.currentDuration = 0

    def createTextToSpeech(self):
        self.postDuration = TextToSpeech("tts/reddit_ask",
                                         {"type": "post", "id": self.post.id,
                                          "text": self.post.title}).getDuration()
        self.currentDuration += self.postDuration

        for comment in self.comments:
            duration = TextToSpeech("tts/reddit_ask",
                                    {"type": "comment", "id": comment.id,
                                     "text": comment.body}).getDuration()
            if self.currentDuration + duration > self.maxDuration:
                break
            self.currentDuration += duration
            self.commentsUsed.append({"comment": comment, "duration": duration})

    def screenshotPost(self):
        RedditScreenshot(self.post.url, post_id=self.post.id, comments=[comment["comment"]
                                                                        for comment in self.commentsUsed])

    def composeVideo(self):
        print("Creating clips for each comment...")

        clips = [createClip("screenshots/reddit_ask/post-" + self.post.id + ".png",
                            AudioFileClip("tts/reddit_ask/post-" + self.post.id + ".mp3"), self.postDuration, self.marginSize)]

        for comment in self.commentsUsed:
            clips.append(createClip("screenshots/reddit_ask/comment-" + comment['comment'].id + ".png",
                                    AudioFileClip("tts/reddit_ask/comment-" + comment['comment'].id + ".mp3"),
                                    comment['duration'], self.marginSize))

        content_overlay = concatenate_videoclips(clips).set_position(("center", "center"))

        background_video = self.getBackgroundVideo()
        final = CompositeVideoClip(
            clips=[background_video, content_overlay],
            size=background_video.size).set_audio(content_overlay.audio)
        final.duration = self.currentDuration
        final.set_fps(background_video.fps)

        print("Rendering final video...")
        bitrate = "8000k"
        threads = "12"
        outputFile = f"final_videos/reddit_ask/" + self.post.id + ".mp4"
        final.write_videofile(
            outputFile,
            codec='mpeg4',
            threads=threads,
            bitrate=bitrate
        )

    def getBackgroundVideo(self):
        random_name = random.choice(os.listdir("background_videos/reddit_ask"))
        backgroundVideo = VideoFileClip(
            filename=f"background_videos/reddit_ask/" + random_name,
            audio=False)

        duration = backgroundVideo.duration
        start = random.randint(0, int(duration) - int(self.currentDuration))
        end = start + self.currentDuration
        return backgroundVideo.subclip(start, end)


def createClip(screenShotFile, audioClip, duration, marginSize):
    imageClip = ImageClip(
        screenShotFile,
        duration=duration,
    ).set_position(("center", "center"))
    imageClip = imageClip.resize(width=(1080 - marginSize))
    videoClip = imageClip.set_audio(audioClip)
    videoClip.fps = 1
    return videoClip
