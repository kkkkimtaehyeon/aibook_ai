import os
from functools import lru_cache

import requests
from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends
from starlette.responses import JSONResponse

from ai_clients.voice_cloning_clients import VoiceCloningClient, ZonosVoiceCloningClient
from schemas.schemas import DubbingRequest
from service.dubbing_generation_service import DubbingGenerationService, ZonosDubbingGenerationService
from utils.logConfig import logger

_ = load_dotenv(find_dotenv())

router = APIRouter()


@lru_cache
def get_dubbing_generation_service() -> DubbingGenerationService:
    api_key = os.getenv("ZYPHRA_API_KEY")
    client: VoiceCloningClient = ZonosVoiceCloningClient(api_key)
    return ZonosDubbingGenerationService(client)


@router.post('/ai/v3/voice-cloning', status_code=200)
async def voice_cloning(request: DubbingRequest,
                        background_tasks: BackgroundTasks,
                        service: DubbingGenerationService = Depends(get_dubbing_generation_service)):
    logger.info('dubbing requested')
    background_tasks.add_task(process_dubbing, request, service)
    return JSONResponse(
        status_code=200,
        content={
            "status": "accepted",
            "message": "Voice cloning request accepted and processing started",
            # "status_check_url": f"/ai/v3/voice-cloning/status/{task_id}"
        }
    )


# async
async def process_dubbing(request: DubbingRequest, service: DubbingGenerationService):
    await service.dub_story(request)
    logger.info('dubbing success')
    requests.post(request.webhook_url, json={"status": "201"})
