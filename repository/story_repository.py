from config.redis_config import redis_client
from schemas.schemas import Story


class StoryRepository:
    def __init__(self):
        self.redis_client = redis_client

    async def find_by_id(self, story_id: str) -> Story:
        base_story = await self.redis_client.get(self._get_base_story_key(story_id))
        contents = await self.redis_client.lrange(self._get_contents_key(story_id), 0, -1)
        return Story(base_story=base_story, contents=contents)

    async def save_base_story(self, story_id: str, base_story: str) -> None:
        await self.redis_client.set(self._get_base_story_key(story_id), base_story)

    async def add_content(self, story_id: str, content: str) -> None:
        await self.redis_client.rpush(self._get_contents_key(story_id), content)

    def _get_base_story_key(self, story_id: str) -> str:
        return f'story:{story_id}:base_story'

    def _get_contents_key(self, story_id: str) -> str:
        return f'story:{story_id}:contents'
