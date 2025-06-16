import base64
from abc import ABC, abstractmethod

import aiohttp
from zyphra import AsyncZyphraClient


class VoiceCloningClient(ABC):

    @abstractmethod
    async def clone_voice(self, reference_audio_url: str, text: str) -> bytes:
        pass


class ZonosVoiceCloningClient(VoiceCloningClient):

    def __init__(self, api_key):
        self.client = AsyncZyphraClient(api_key=api_key)
        self.api_key = api_key

    def _get_client(self):
        return AsyncZyphraClient(api_key=self.api_key)

    async def clone_voice(self, reference_audio_url: str, text: str) -> bytes:
        base64_audio = await self._encode_audio_base64(reference_audio_url)
        audio_bytes: bytes = await self._generate_speech(base64_audio, text)
        return audio_bytes

    async def _encode_audio_base64(self, reference_audio_url: str):
        async with aiohttp.ClientSession() as client:
            async with client.get(reference_audio_url) as response:
                audio_file = await response.read()
        return base64.b64encode(audio_file).decode('utf-8')

    async def _generate_speech(self, base64_audio, text) -> bytes:
        async with self._get_client() as client:
            audio_data = await client.audio.speech.create(
                text=text,
                language_iso_code='ko',
                speaking_rate=15,
                speaker_audio=base64_audio,
                mime_type="audio/webm",
                model="zonos-v0.1-transformer"
            )
        return audio_data
