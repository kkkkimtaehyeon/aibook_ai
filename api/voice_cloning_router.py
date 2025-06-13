import asyncio
import os

import httpx
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, BackgroundTasks

from ai_clients.voice_cloning_clients import Zyphra
from schemas.schemas import DubbingRequest
from utils.logConfig import logger

_ = load_dotenv(find_dotenv())

router = APIRouter()

api_key = os.getenv("ZYPHRA_API_KEY")


@router.post('/ai/v3/voice-cloning', status_code=202)
async def voice_cloning(request: DubbingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_dubbing_v3, request)
    logger.debug(f"Voice cloning request received: webhook url: {request.webhook_url}")
    return


# async
async def process_dubbing_v3(request: DubbingRequest):
    zyphra = Zyphra(api_key)
    base64_audio = zyphra.get_base64_audio(request.voice_audio_url)
    tasks = []

    async with httpx.AsyncClient() as client:
        async def process_page(page_id, content, pre_signed_url):
            try:
                audio_bytes: bytes = await zyphra.generate_speech_async(base64_audio, content)

                response = await client.put(pre_signed_url, content=audio_bytes, headers={"Content-Type": "audio/wav"})
                if response.status_code != 200:
                    logger.error(f"Failed to upload audio to S3 for page {page_id}: {response.status_code}")
                else:
                    logger.debug(f"audio uploaded: page({page_id})")
            except Exception as e:
                logger.exception(f"Error processing page {page_id}: {str(e)}")

        # 각 페이지에 대해 Task 생성
        for page_id, content_and_url in request.story_page_map.items():
            tasks.append(process_page(page_id, content_and_url.content, content_and_url.pre_signed_url))

        # 병렬 실행
        await asyncio.gather(*tasks)

        await client.post(request.webhook_url, json={"status": "200"})
