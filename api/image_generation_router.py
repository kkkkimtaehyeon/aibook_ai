import os

from fastapi import APIRouter, Depends

from ai_clients.image_clients import GeminiImageClient
from api.story_generation_router import get_story_generation_service
from service.image_generation_service import ImageGenerationService, GeminiImageGenerationService
from service.story_generation_service import StoryGenerationService

router = APIRouter()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
image_client = GeminiImageClient(GEMINI_API_KEY)


def get_image_generation_service(
        story_service: StoryGenerationService = Depends(get_story_generation_service)) -> ImageGenerationService:
    return GeminiImageGenerationService(image_client, story_service)


@router.post("/ai/v3/stories/{story_id}/image-generation")
async def generate_image(story_id: str,
                         image_generation_service: ImageGenerationService = Depends(get_image_generation_service)):
    base64Image = await image_generation_service.generate_image(story_id)
    return base64Image
