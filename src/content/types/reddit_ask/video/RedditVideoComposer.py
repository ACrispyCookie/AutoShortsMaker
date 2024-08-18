import os
import random

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

marginSize = 150


class RedditVideoComposer:

    def __init__(self, post, comments, totalDuration, background_path, final_path):
        self.post = post
        self.comments = comments
        self.totalDuration = totalDuration
        self.background_path = background_path
        self.image_path = os.path.dirname(post.image) + "/"
        self.tts_path = os.path.dirname(post.tts) + "/"
        self.final_path = final_path

    def composeVideo(self, bitrate, threads):
        print("Creating clips for each comment...")

        clips = [createClip(self.image_path + "post-" + self.post.id + ".png",
                            AudioFileClip(self.tts_path + "post-" + self.post.id + ".mp3"),
                            self.post.tts_duration, marginSize)]

        for comment in self.comments:
            clips.append(createClip(comment.image,
                                    AudioFileClip(comment.tts),
                                    comment.tts_duration, marginSize))

        content_overlay = concatenate_videoclips(clips).set_position(("center", "center"))

        background_video = self.getBackgroundVideo()
        final = CompositeVideoClip(
            clips=[background_video, content_overlay],
            size=background_video.size).set_audio(content_overlay.audio)
        final.tts_duration = self.totalDuration
        final.set_fps(background_video.fps)

        print("Rendering final video...")
        outputFile = self.final_path + self.post.id + ".mp4"
        final.write_videofile(
            outputFile,
            codec='mpeg4',
            threads=threads,
            bitrate=bitrate
        )

    def getBackgroundVideo(self):
        random_name = random.choice(os.listdir(self.background_path))
        backgroundVideo = VideoFileClip(
            filename=self.background_path + random_name,
            audio=False)

        duration = backgroundVideo.duration
        start = random.randint(0, int(duration) - int(self.totalDuration))
        end = start + self.totalDuration
        return backgroundVideo.subclip(start, end)


def createClip(screenShotFile, audioClip, duration, margin_size):
    imageClip = ImageClip(
        screenShotFile,
        duration=duration,
    ).set_position(("center", "center"))
    imageClip = imageClip.resize(width=(1080 - margin_size))
    videoClip = imageClip.set_audio(audioClip)
    videoClip.fps = 1
    return videoClip
