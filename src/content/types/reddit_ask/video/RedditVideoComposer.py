import os
import random
from typing import List

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip, VideoClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from content.types.reddit_ask.wrappers.RedditComment import RedditComment
from content.types.reddit_ask.wrappers.RedditPost import RedditPost

marginSize = 150


class RedditVideoComposer:

    def __init__(self, post: RedditPost, comments: List[RedditComment], total_duration: int, background_path: str, final_path: str):
        self.post: RedditPost = post
        self.comments: List[RedditComment] = comments
        self.total_duration: int = total_duration
        self.background_path: str = background_path
        self.image_path: str = os.path.dirname(post.image) + "/"
        self.tts_path: str = os.path.dirname(post.tts) + "/"
        self.final_path: str = final_path

    def compose_video(self, bitrate, threads):
        print("Creating clips for each comment...")

        clips: List[VideoClip] = [create_clip(self.image_path + "post-" + str(self.post.id) + ".png",
                             AudioFileClip(self.tts_path + "post-" + str(self.post.id) + ".mp3"),
                             self.post.tts_duration, marginSize)]

        for comment in self.comments:
            clips.append(create_clip(comment.image,
                                     AudioFileClip(comment.tts),
                                     comment.tts_duration, marginSize))

        content_overlay: VideoClip = concatenate_videoclips(clips).set_position(("center", "center"))

        background_video: VideoClip = self.get_background_video()
        final: VideoClip = CompositeVideoClip(
            clips=[background_video, content_overlay],
            size=background_video.size).set_audio(content_overlay.audio)
        final.tts_duration = self.total_duration
        final.set_fps(background_video.fps)

        print("Rendering final video...")
        output_file: str = self.final_path + str(self.post.id) + ".mp4"
        final.write_videofile(
            output_file,
            codec='mpeg4',
            threads=threads,
            bitrate=bitrate
        )

    def get_background_video(self) -> VideoClip:
        random_name: str = random.choice(os.listdir(self.background_path))
        background_video: VideoClip = VideoFileClip(
            filename=self.background_path + random_name,
            audio=False)

        duration: int = background_video.duration
        start: int = random.randint(0, int(duration) - int(self.total_duration))
        end: int = start + self.total_duration
        return background_video.subclip(start, end)


def create_clip(screen_shot_file: str, audio_clip: AudioFileClip, duration: int, margin_size: int) -> VideoClip:
    image_clip = ImageClip(
        screen_shot_file,
        duration=duration,
    ).set_position(("center", "center"))
    image_clip = image_clip.resize(width=(1080 - margin_size))
    video_clip: VideoClip = image_clip.set_audio(audio_clip)
    video_clip.fps = 1
    return video_clip
