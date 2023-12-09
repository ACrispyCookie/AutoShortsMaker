import os
import random

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from src.screenshot.RedditScreenshot import RedditScreenshot
from src.screenshot.RedditTemplateImage import RedditTemplateImage
from src.tts.TextToSpeech import TextToSpeech

marginSize = 80
maxCommentLength = 100


class RedditVideoComposer:

    def __init__(self, post, comments, maxDuration=58):
        self.post = post
        self.comments = comments
        self.commentsUsed = []
        self.currentDuration = 0
        self.maxDuration = maxDuration

    def createTextToSpeech(self):
        self.post.setDuration(TextToSpeech(self.post).getDuration())
        self.currentDuration += self.post.tts_duration

        for comment in self.comments:
            if not isCommentValid(comment):
                continue
            duration = TextToSpeech(comment).getDuration()
            if self.currentDuration + duration > self.maxDuration:
                break
            comment.setDuration(duration)
            self.currentDuration += duration
            self.commentsUsed.append(comment)

    def screenshotPost(self):
        RedditTemplateImage(self.post).create()
        for comment in self.commentsUsed:
            RedditTemplateImage(comment).create()

    def composeVideo(self):
        print("Creating clips for each comment...")

        clips = [createClip("screenshots/reddit_ask/post-" + self.post.id + ".png",
                            AudioFileClip("tts/reddit_ask/post-" + self.post.id + ".mp3"),
                            self.post.tts_duration, marginSize)]

        for comment in self.commentsUsed:
            clips.append(createClip(comment.screenshot,
                                    AudioFileClip(comment.tts),
                                    comment.tts_duration, marginSize))

        content_overlay = concatenate_videoclips(clips).set_position(("center", "center"))

        background_video = self.getBackgroundVideo()
        final = CompositeVideoClip(
            clips=[background_video, content_overlay],
            size=background_video.size).set_audio(content_overlay.audio)
        final.tts_duration = self.currentDuration
        final.set_fps(background_video.fps)

        print("Rendering final video...")
        bitrate = "8000k"
        threads = "24"
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


def isCommentValid(comment):
    if comment.body == '[deleted]' or comment.body == '[removed]' or comment.body == '':
        return False
    if len(comment.body) > maxCommentLength:
        return False
    return True


def createClip(screenShotFile, audioClip, duration, margin_size):
    imageClip = ImageClip(
        screenShotFile,
        duration=duration,
    ).set_position(("center", "center"))
    imageClip = imageClip.resize(width=(1080 - margin_size))
    videoClip = imageClip.set_audio(audioClip)
    videoClip.fps = 1
    return videoClip
