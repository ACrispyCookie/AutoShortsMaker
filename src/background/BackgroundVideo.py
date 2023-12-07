import moviepy.video.fx.all as vfx
import moviepy.editor as mp


class BackgroundVideo:

    def __init__(self, folder, name):
        self.folder = folder
        self.name = name

    def download(self):
        raise NotImplementedError("Subclass must implement abstract method")


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
