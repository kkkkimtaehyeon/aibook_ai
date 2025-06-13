from abc import ABC, abstractmethod

from ai_clients.image_clients import ImageClient
from service.story_generation_service import StoryGenerationService


class ImageGenerationService(ABC):
    @abstractmethod
    async def generate_image(self, story_id: str) -> str:  # base64 encoded image string
        pass


class GeminiImageGenerationService(ImageGenerationService):
    def __init__(self, image_client: ImageClient, story_generation_service: StoryGenerationService):
        self.image_client = image_client
        self.story_generation_service = story_generation_service

    async def generate_image(self, story_id: str) -> str:
        summary = await self.story_generation_service.summarize_story(story_id)
        image_generation_prompt = self._get_image_generation_prompt(summary)
        return self.image_client.generate_image(image_generation_prompt)

    def _get_image_generation_prompt(self, story_summary: str):
        return f"fairytale cover, for children, the summary of the story: {story_summary}"
