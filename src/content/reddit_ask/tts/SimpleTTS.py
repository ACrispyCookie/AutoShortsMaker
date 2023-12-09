import pyttsx3
from moviepy.audio.io.AudioFileClip import AudioFileClip

from src.content.reddit_ask.tts.TextToSpeech import TextToSpeech


class SimpleTTS(TextToSpeech):

    def __init__(self, reddit_content):
        super().__init__(reddit_content)
        self.engine = engine_init()
        self.engine.save_to_file(self.content.body, self.content.tts)

    def create(self):
        self.engine.runAndWait()
        return self

    def getDuration(self):
        file_path = self.content.tts
        return AudioFileClip(file_path).duration


def engine_init():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', 'english+f3')
    return engine
