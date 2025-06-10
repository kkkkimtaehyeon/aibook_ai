from fastapi import APIRouter

from repository.StoryRepository import StoryRepository
from repository.interface.StoryRepositoryInterface import StoryRepositoryInterface
from schemas.schemas import StoryGenerateRequestV2
from service.StoryGenerationServiceV2 import StoryGenerationServiceV2

router = APIRouter()
story_repository: StoryRepositoryInterface = StoryRepository()
story_service_v2 = StoryGenerationServiceV2(story_repository)


def get_story_generate_service_v2():
    return story_service_v2


@router.post("/ai/v2/stories/{story_id}/pages/{page_number}/generate")
async def generate_story_v2(story_id: str, page_number: int, request: StoryGenerateRequestV2):
    if page_number == 1:
        # 1페이지일 때는 base_story가 필요.
        if not request.base_story:
            raise ValueError("base_story is required for the first page.")
        story = await story_service_v2.set_base_story(story_id, request.base_story)
        return story_service_v2.generate_content(story, page_number)
    else:
        # 2페이지 이상일 때는 selected_sentence가 필요.
        if not request.selected_sentence:
            raise ValueError("selected_sentence is required for subsequent pages.")
        story = await story_service_v2.add_content(story_id, request.selected_sentence)
        return story_service_v2.generate_content(story, page_number)
