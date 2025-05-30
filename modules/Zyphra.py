import base64
import os
import requests

from zyphra import ZyphraClient, AsyncZyphraClient


class Zyphra:
    def __init__(self, api_key):
        self.client = ZyphraClient(api_key=api_key)
        self.api_key = api_key

    def get_async_client(self):
        return AsyncZyphraClient(api_key=self.api_key)

    def get_base64_audio(self, reference_audio_url):
        audio_file = requests.get(reference_audio_url).content
        encoded_audio = base64.b64encode(audio_file).decode('utf-8')
        return encoded_audio

    def generate_speech(self, base64_audio, text) -> bytes:
        audio_data = self.client.audio.speech.create(
            text=text,
            language_iso_code='ko',
            speaking_rate=15,
            speaker_audio=base64_audio,
            model="zonos-v0.1-transformer"
        )
        return audio_data

    async def generate_speech_async(self, base64_audio, text) -> bytes:
        async with self.get_async_client() as client:
            audio_data = await client.audio.speech.create(
                text=text,
                language_iso_code='ko',
                speaking_rate=15,
                speaker_audio=base64_audio,
                model="zonos-v0.1-transformer"
            )
        return audio_data
