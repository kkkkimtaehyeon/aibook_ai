import os
from functools import lru_cache

from dotenv import find_dotenv, load_dotenv
from fastapi import APIRouter, Depends

from ai_clients.llm_clients import GptLlmClient
from repository.story_repository import StoryRepository
from schemas.schemas import StoryGenerateRequest
from service.story_generation_service import StoryGenerationService, GptStoryGenerationService

router = APIRouter()
_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


@lru_cache
def get_story_generation_service() -> StoryGenerationService:
    return GptStoryGenerationService(GptLlmClient(OPENAI_API_KEY), StoryRepository())


@router.post("/ai/v2/stories/{story_id}/pages/{page}/generate")
async def generate_story(story_id: str,
                         page: int,
                         request: StoryGenerateRequest,
                         story_service: StoryGenerationService = Depends(get_story_generation_service)):
    return await story_service.generate_story(story_id, page, request)
