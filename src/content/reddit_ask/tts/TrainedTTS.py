from src.content.reddit_ask.tts.TextToSpeech import TextToSpeech
import torch
from TTS.api import TTS

class TrainedTTS(TextToSpeech):

    def __init__(self, reddit_content):
        super().__init__(reddit_content)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/en/ljspeech/glow-tts").to(self.device)

    def create(self):
        self.tts.tts_to_file(text=self.content.body, file_path=self.content.tts)
        return self
