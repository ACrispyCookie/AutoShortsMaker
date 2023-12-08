import pyttsx3
from moviepy.audio.io.AudioFileClip import AudioFileClip


class TextToSpeech:

    def __init__(self, element=None):
        self.engine = engine_init()
        self.save_path = element.tts
        self.element = element
        self.engine.save_to_file(element.body, self.save_path)
        self.engine.runAndWait()

    def getDuration(self):
        file_path = self.save_path
        return AudioFileClip(file_path).duration


def engine_init():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', 'english+f3')
    return engine
