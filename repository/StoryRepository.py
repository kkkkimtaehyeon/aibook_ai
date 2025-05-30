import json

from config.redis_config import redis_client
from repository.interface.StoryRepositoryInterface import StoryRepositoryInterface
from service.StoryGenerationServiceV2 import TempStory


class StoryRepository(StoryRepositoryInterface):

    def __init__(self):
        self.redis_client = redis_client
        self.repository: dict[str, TempStory] = {}

    async def save(self, key, value):
        await self.redis_client.set(key, value)

    async def get(self, key):
        return await self.redis_client.get(key)

    async def save_story(self, story_id: str, story: TempStory):
        story_dict = story.to_dict()
        story_json_str = json.dumps(story_dict, ensure_ascii=False).encode("utf-8")
        await self.save(story_id, story_json_str)

    async def save_base_story(self, story_id: str, base_story: str):
        story = TempStory(base_story)
        await self.save_story(story_id, story)
        return story

    async def save_selected_sentence(self, story_id: str, selected_sentence: str):
        story = await self.find_story_by_id(story_id)
        story.add_content(selected_sentence)
        await self.save_story(story_id, story)
        return story

    async def find_story_by_id(self, story_id: str):
        story_json_str = await self.get(story_id)
        story_dict = json.loads(story_json_str)
        story = TempStory.from_dict(story_dict)
        return story

    async def find_by_id(self, story_id: str):
        try:
            story = await self.get(story_id)
            return story
        except KeyError:
            raise ValueError(f"story id '{story_id}' not found")

    # def find_by_id(self, story_id: str):
    #     try:
    #         story = self.repository[story_id]
    #         return story
    #     except KeyError:
    #         raise ValueError(f"story id '{story_id}' not found")

    def delete_by_id(self, story_id: str):
        story = self.find_by_id(story_id)
        del self.repository[story_id]
