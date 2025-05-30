import base64
import asyncio
from httpx import AsyncClient
import requests
from zyphra import AsyncZyphraClient

from service.interface.voice_cloning_service import VoiceCloningService


class ZonosVoiceCloningService(VoiceCloningService):

    def __init__(self, client):
        self.client = client
        self.TTS_END_POINT = "http://api.zyphra.com/v1/audio/text-to-speech"
        pass

    def get_speaker_audio(self, reference_audio_url: str) -> str:
        audio_file = requests.get(reference_audio_url).content
        encoded_audio = base64.b64encode(audio_file).decode('utf-8')
        return encoded_audio
        pass

    async def generate_speeches(self, base64_audio: str, story_pages: dict[str, str]):
        tasks = self.get_tasks(base64_audio, story_pages)

    def get_tasks(self, base64_audio: str, story_pages: dict[str, str]) -> dict:
        headers = {
            "X-API-Key": self.client.api_key,
            "Content-Type": "application/json"
        }
        tasks = {}
        for page_id, content in story_pages.items():
            body = {
                "text": content,
                "speaking_rate": 15,
                "speaker_audio": base64_audio,
            }
            async with AsyncClient() as client:
                tasks[page_id] = client.post(self.TTS_END_POINT, json=body, headers=headers)
        return tasks

    async def generate_speech(self, base64_audio: str, text: str) -> bytes:
        headers = {
            "X-API-Key": self.client.api_key,
            "Content-Type": "application/json"
        }
        body = {
            "text": text,
            "speaking_rate": 15,
            "speaker_audio": base64_audio,
        }
        async with AsyncClient() as client:
            response = await client.post(self.TTS_END_POINT, json=body, headers=headers)
