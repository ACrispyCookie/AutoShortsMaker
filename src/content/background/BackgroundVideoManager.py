import os
import moviepy.video.fx.all as vfx
import moviepy.editor as mp
from content.background.UrlVideoDownloader import UrlVideoDownloader


def getFirstVideoName(folder):
    name = "video_0"
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        name = name.removesuffix("0") + str(len(os.listdir(folder)))
    return name


def downloadBackgroundVideos(url, playlist, folder):
    url = url
    playlist = playlist

    UrlVideoDownloader(url=url, playlist=playlist,
                       folder=folder, name=getFirstVideoName(folder)).download()


def cropBackgroundVideos(folder):
    for file in os.listdir(folder):
        if file.endswith(".webm"):
            cropBackgroundVideo(folder + file,
                                folder + file.removesuffix(".webm") + "_final.webm")
            if os.path.exists(folder + file.removesuffix(".webm") + "_final.webm"):
                os.rename(folder + file.removesuffix(".webm") + "_final.webm", folder + file)


def cropBackgroundVideo(input_path, output_path):
    clip = mp.VideoFileClip(input_path)
    (w, h) = clip.size
    new_width = int(h * 9 / 16)
    if new_width == w:
        clip.close()
        return

    x1, x2 = (w - new_width) // 2, (w + new_width) // 2
    y1, y2 = 0, h

    clip_cropped = vfx.crop(clip, x1=x1, x2=x2, y1=y1, y2=y2)
    clip_cropped.write_videofile(output_path)
    clip_cropped.close()
    clip.close()