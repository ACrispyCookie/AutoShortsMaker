from abc import ABC, abstractmethod
from enum import Enum
from unittest.mock import DEFAULT

from moviepy.audio.io.AudioFileClip import AudioFileClip

class TTSMode(Enum):
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
        file_path: str = self.filename
        return AudioFileClip(file_path).duration
