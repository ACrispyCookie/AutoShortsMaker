from abc import ABC, abstractmethod
from moviepy.audio.io.AudioFileClip import AudioFileClip


class TextToSpeech(ABC):

    def __init__(self, reddit_content):
        self.content = reddit_content

    @abstractmethod
    def create(self):
        raise NotImplementedError

    def getDuration(self):
        file_path = self.content.tts
        return AudioFileClip(file_path).duration
