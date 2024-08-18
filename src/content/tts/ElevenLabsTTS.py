import pyttsx3
from pyttsx3 import Engine

from src.content.tts.TextToSpeech import TextToSpeech

class SimpleTTS(TextToSpeech):

    def __init__(self, content: str, filename: str):
        super().__init__(content, filename)
        self.engine: Engine = engine_init()
        self.engine.save_to_file(self.content, self.filename)

    def create(self):
        self.engine.runAndWait()
        return self


def engine_init() -> Engine:
    engine: Engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', 'english+f3')
    return engine
