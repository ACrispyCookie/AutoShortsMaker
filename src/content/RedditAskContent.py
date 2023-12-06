from src.content.Content import Content
import os
import praw
from src.background.BackgroundUrlVideo import BackgroundUrlVideo
import moviepy.editor as mp


class RedditAskContent(Content):

    def __init__(self):
        super().__init__("RedditAsk")

    def create(self):
        #self.download_background_video()


    def download_background_video(self):
        print("Downloading background video...")
        if not os.path.exists("background_videos"):
            os.mkdir("background_videos")
        BackgroundUrlVideo(url="https://www.youtube.com/watch?v=JlPEb6WNuDI",
                           folder="background_videos", name="background_video.mp4").download()

        print("Resizing background video...")
        resize_background_video("background_videos/background_video.mp4",
                                "background_videos/background_video_final.mp4", 1080, 1920)
        os.rename("background_videos/background_video_final.mp4", "background_videos/background_video.mp4")


def resize_background_video(input_path, output_path, new_width, new_height):
    clip = mp.VideoFileClip(input_path)
    clip_resized = clip.resize(height=new_height, width=new_width)
    clip_resized.write_videofile(output_path)
    clip_resized.close()
    clip.close()
