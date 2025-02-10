from fastapi import APIRouter
from schemas.schemas import StoryGenerateRequest, StoryGenerateResponse
from modules.gpt_works import generate_story, generate_story_prompt, generate_base_story_prompt

router = APIRouter()


@router.post("/api/story/generate")
async def generate_stories(request: StoryGenerateRequest) -> StoryGenerateResponse:
    if request.page_number == 1:
        prompt = generate_base_story_prompt(request.source)
    else:
        prompt = generate_story_prompt(request.source, request.page_number)

    response = StoryGenerateResponse(**generate_story(prompt))
    return response

