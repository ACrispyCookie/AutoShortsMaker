from typing import Dict, Any

import requests
from requests import Response

from tools.tts.TextToSpeech import TextToSpeech

api_key: str

class ElevenLabsTTS(TextToSpeech):

    def __init__(self, content: str, filename: str, voice: str):
        super().__init__(content, filename)
        self.voice_id: str = voice

    def create(self) -> TextToSpeech:
        chunk_size: int = 1024
        url: str = "https://api.elevenlabs.io/v1/text-to-speech/" + self.voice_id

        headers: Dict[str, str] = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data: Dict[str, Any] = {
            "text": self.content,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response: Response = requests.post(url, json=data, headers=headers)
        with open(self.filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        return self


def set_key(key: str):
    global api_key
    api_key = key