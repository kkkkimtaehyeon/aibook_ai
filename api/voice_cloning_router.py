import asyncio
import base64
import os
import time

import httpx
import requests
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, BackgroundTasks

from modules.Zyphra import Zyphra
from schemas.schemas import VoiceCloningRequest, VoiceCloningResponse, DubbingRequest
from utils.logConfig import logger

_ = load_dotenv(find_dotenv())

router = APIRouter()

api_key = os.getenv("ZYPHRA_API_KEY")


# 백그라운드에서 더빙 처리하고 우선 202 응답
@router.post('/ai/v1/voice-cloning', status_code=202)
async def voice_cloning(request: DubbingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_dubbing_v2, request)
    logger.debug(f"Voice cloning request received: webhook url: {request.webhook_url}")
    return


@router.post('/ai/v2/voice-cloning', status_code=202)
async def voice_cloning(request: VoiceCloningRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_dubbing_v1, request)
    logger.debug(f"Voice cloning request received: webhook url: {request.webhook_url}")
    return


@router.post('/ai/v3/voice-cloning', status_code=202)
async def voice_cloning(request: DubbingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_dubbing_v3, request)
    logger.debug(f"Voice cloning request received: webhook url: {request.webhook_url}")
    return


async def process_dubbing_v1(request: VoiceCloningRequest):
    zyphra = Zyphra(api_key)
    base64_audio = zyphra.get_base64_audio(request.audio_url)
    total_tts_time = 0

    story_dubbing_dict = {}
    for page_id, content in request.story_page_map.items():
        # tts 생성
        start = time.time()
        audio_bytes: bytes = zyphra.generate_speech(base64_audio, content)
        end = time.time()
        total_tts_time += end - start

        story_dubbing_dict[page_id] = base64.b64encode(audio_bytes).decode('utf-8')
        logger.debug(f"page({page_id}) dubbing processed: {story_dubbing_dict[page_id] is not None}")
    # 더빙 작업 완료 시 api 서버에 완료 처리 (POST 요청)
    response = VoiceCloningResponse(storyDubbingMap=story_dubbing_dict)
    logger.debug(f"response: {response.model_dump(by_alias=True)}")

    logger.debug(f"Total TTS processing time: {total_tts_time} seconds")
    requests.post(request.webhook_url, json=response.model_dump(by_alias=True))


async def process_dubbing_v2(request: DubbingRequest):
    zyphra = Zyphra(api_key)
    base64_audio = zyphra.get_base64_audio(request.voice_audio_url)
    total_tts_time = 0

    for page_id, content_and_url in request.story_page_map.items():
        content = content_and_url.content
        pre_signed_url = content_and_url.pre_signed_url
        # tts 생성
        start = time.time()
        audio_bytes: bytes = zyphra.generate_speech(base64_audio, content)
        end = time.time()
        total_tts_time += end - start

        logger.debug(f"audio generated: {content}")
        # s3에 업로드
        http_response = requests.put(pre_signed_url, data=audio_bytes, headers={"Content-Type": "audio/wav"})
        if http_response.status_code != 200:
            logger.error(f"Failed to upload audio to S3 for page {page_id}: {http_response.status_code}")
            continue
        logger.debug(f"audio uploaded: page({page_id})")
    # 더빙 작업 완료 시 api 서버에 완료 처리 (POST 요청)
    logger.debug(f"Total TTS processing time: {total_tts_time} seconds")
    requests.post(request.webhook_url, json={"status": "completed"})


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
