import os
import moviepy.video.fx.all as vfx
import moviepy.editor as mp
from moviepy.video.VideoClip import VideoClip

from content.background.UrlVideoDownloader import UrlVideoDownloader


def get_first_video_name(folder: str) -> str:
    name: str = "video_0"
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        name: str = name.removesuffix("0") + str(len(os.listdir(folder)))
    return name


def download_background_videos(url: str, playlist: bool, folder: str):
    UrlVideoDownloader(url=url, playlist=playlist,
                       folder=folder, name=get_first_video_name(folder)).download()


def crop_background_videos(folder: str):
    for file in os.listdir(folder):
        if file.endswith(".webm"):
            crop_background_video(folder + file,
                                  folder + file.removesuffix(".webm") + "_final.webm")
            if os.path.exists(folder + file.removesuffix(".webm") + "_final.webm"):
                os.rename(folder + file.removesuffix(".webm") + "_final.webm", folder + file)


def crop_background_video(input_path: str, output_path: str):
    clip: VideoClip = mp.VideoFileClip(input_path)
    (w, h) = clip.size
    new_width: int = int(h * 9 / 16)
    if new_width == w:
        clip.close()
        return

    x1, x2 = (w - new_width) // 2, (w + new_width) // 2
    y1, y2 = 0, h

    clip_cropped: VideoClip = vfx.crop(clip, x1=x1, x2=x2, y1=y1, y2=y2)
    clip_cropped.write_videofile(output_path)
    clip_cropped.close()
    clip.close()