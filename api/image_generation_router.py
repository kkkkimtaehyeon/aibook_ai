import os

from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Depends
from openai import OpenAI

from repository.StoryRepository import StoryRepository
from schemas.schemas import ImageGenerationRequest
from service.ImageGenerationService import ImageGenerationService
from service.ImageGenerationServiceV2 import ImageGenerationServiceV2
from service.StoryGenerationService import StoryGenerationService
from service.StoryGenerationServiceV2 import StoryGenerationServiceV2
from service.interface.ImageGenerationServiceInterface import ImageGenerationServiceInterface
from service.interface.StoryGenerationServiceInterface import StoryGenerationServiceInterface
from utils.logConfig import logger

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


# @router.post("/v1/api/image-generation")
# async def image_generation(request: ImageGenerationRequest,
#                            image_generation_service: ImageGenerationServiceInterface = Depends(
#                                ImageGenerationService),
#                            story_generation_service: StoryGenerationServiceInterface = Depends(
#                                get_story_generate_service)):
#     source: str = ", ".join(request.contents)
#     prompt = story_generation_service.generate_image_generation_prompt(source)
#     # prompt = "A heartwarming scene in a park on a special day. A young person is walking hand in hand with their best friend, a timid dog named Sundol. The dog initially looks fearful but starts to feel more secure with the person beside them. They pause to admire colorful flowers, with the person encouraging the dog to overcome its fears. In the background, there’s a large tree and a gentle pathway leading into a small forest. The atmosphere is filled with warmth and friendship, capturing the essence of courage and companionship."
#     logger.debug(f"prompt : {prompt}")
#     json_response = image_generation_service.generate_image(prompt)
#     logger.debug(json_response)
#     return json_response


@router.post("/v2/ai/stories/{story_id}/image-generation")
async def generate_image(story_id: str):
    base64_image = await image_generation_service_v2.generate_image(story_id)
    return {
        "base64Image": base64_image
    }
