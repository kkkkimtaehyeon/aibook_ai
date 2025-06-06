import os

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter
from openai import OpenAI

from repository.StoryRepository import StoryRepository
from service.ImageGenerationServiceV2 import ImageGenerationServiceV2
from service.StoryGenerationService import StoryGenerationService
from service.interface.StoryGenerationServiceInterface import StoryGenerationServiceInterface
from service.image_generate_service import generate_image

router = APIRouter()

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
repository = StoryRepository()
story_service = StoryGenerationService(client, repository)
image_generation_service_v2 = ImageGenerationServiceV2(repository)


def get_image_generation_service_v2():
    return image_generation_service_v2


def get_story_generate_service() -> StoryGenerationServiceInterface:
    return story_service


@router.post("/v2/ai/stories/{story_id}/image-generation")
async def generate_image(story_id: str):
    base64_image = await image_generation_service_v2.generate_image(story_id)
    return {
        "base64Image": base64_image
    }


@router.post("/v3/ai/stories/{story_id}/image-generation")
async def generate_image_v3(story_id: str):
    story = repository.find_story_by_id(story_id)
    img_generation_prompt = story_service.get_image_generation_prompt(story.contents)
    base64_img = generate_image(img_generation_prompt["summary"])
    return {
        "base64Image": base64_img
    }
