import base64
from utils.logConfig import logger
import os

import requests
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, BackgroundTasks

from modules.Zyphra import Zyphra
from schemas.schemas import VoiceCloningRequest, VoiceCloningResponse

_ = load_dotenv(find_dotenv())

router = APIRouter()

api_key = os.getenv("ZYPHRA_API_KEY")


# 백그라운드에서 더빙 처리하고 우선 202 응답
@router.post('/api/voice-cloning', status_code=202)
async def voice_cloning(request: VoiceCloningRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_dubbing, request)
    logger.debug(f"Voice cloning request received: webhook url: {request.webhook_url}")
    return


# 더빙 처리
async def process_dubbing(request: VoiceCloningRequest):
    zyphra = Zyphra(api_key)
    base64_audio = zyphra.get_base64_audio(request.audio_url)

    story_dubbing_dict = {}
    for page_id, content in request.story_page_map.items():
        audio_bytes: bytes = zyphra.generate_speech(base64_audio, content)
        story_dubbing_dict[page_id] = base64.b64encode(audio_bytes).decode('utf-8')
        logger.debug(f"page({page_id}) dubbing processed: {story_dubbing_dict[page_id] is not None}")
    # 더빙 작업 완료 시 api 서버에 완료 처리 (POST 요청)
    response = VoiceCloningResponse(storyDubbingMap=story_dubbing_dict)
    logger.debug(f"response: {response.model_dump(by_alias=True)}")

    requests.post(request.webhook_url, json=response.model_dump(by_alias=True))
