import asyncio
from abc import ABC, abstractmethod

import httpx

from ai_clients.voice_cloning_clients import VoiceCloningClient
from schemas.schemas import DubbingRequest, DubbingContentAndPreSignedUrl
from utils.logConfig import logger


class DubbingGenerationService(ABC):
    @abstractmethod
    async def dub_story(self, request: DubbingRequest):
        pass


class ZonosDubbingGenerationService(DubbingGenerationService):
    def __init__(self, voice_cloning_client: VoiceCloningClient):
        self.voice_cloning_client = voice_cloning_client

    async def dub_story(self, request: DubbingRequest):
        reference_audio_url = request.voice_audio_url
        tasks = []

        async with httpx.AsyncClient() as client:
            for page_id, content_and_url in request.story_page_map.items():
                tasks.append(self._dub_story_page(client, reference_audio_url, content_and_url))

            # 병렬 실행
            await asyncio.gather(*tasks)

    async def _dub_story_page(self, client, reference_audio_url: str, content_and_url: DubbingContentAndPreSignedUrl):
        audio_byte: bytes = await self.voice_cloning_client.clone_voice(reference_audio_url, content_and_url.content)
        await self._upload_dubbing(client, content_and_url.pre_signed_url, audio_byte)

    async def _upload_dubbing(self, client, pre_signed_url: str, audio_bytes: bytes):
        response = await client.put(url=pre_signed_url, content=audio_bytes, headers={"Content-Type": "audio/webm"})
        if response.status_code != 200:
            logger.error(f"Failed to upload audio to S3 for page : {response.status_code}")
            # TODO: 재시도
