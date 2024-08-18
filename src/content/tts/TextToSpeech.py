from abc import ABC, abstractmethod
from enum import Enum

from moviepy.audio.io.AudioFileClip import AudioFileClip

class TTSType(Enum):
    DEFAULT = 1
    ELEVEN_LABS = 2


class TextToSpeech(ABC):

    def __init__(self, content: str, filename: str):
        self.content = content
        self.filename = filename

    @abstractmethod
    def create(self):
        raise NotImplementedError

    def get_duration(self) -> float:
        file_path = self.filename
        return AudioFileClip(file_path).duration
