from abc import ABC, abstractmethod
from typing import Dict, List

from ai_clients.llm_clients import LlmClient
from repository.story_repository import StoryRepository
from schemas.schemas import Story, StoryGenerateRequest


class StoryGenerationService(ABC):

    @abstractmethod
    async def generate_story(self, story_id: str, page: int, request: StoryGenerateRequest):
        pass

    @abstractmethod
    async def save_base_story(self, story_id: str, base_story: str):
        pass

    @abstractmethod
    async def add_selected_content(self, story_id, selected_content: str):
        pass

    @abstractmethod
    async def summarize_story(self, story_id: str) -> str:
        pass

    @abstractmethod
    def generate_content_options(self, story_id: str, page: int) -> List:
        pass

    @abstractmethod
    def get_first_content_prompt(self, base_story: str):
        pass

    @abstractmethod
    def get_content_prompt(self, story_sofar: str, page: int):
        pass

    @abstractmethod
    def get_story_summary_prompt(self, full_story: str):
        pass


class GptStoryGenerationService(StoryGenerationService):
    async def generate_story(self, story_id: str, page: int, request: StoryGenerateRequest) -> List:
        if page == 1:
            # 1페이지일 때는 base_story 저장.
            await self.save_base_story(story_id, request.base_story)
        else:
            # 2페이지 이상일 때는 selected_sentence 저장.
            await self.add_selected_content(story_id, request.selected_sentence)
        return await self.generate_content_options(story_id, page)

    def __init__(self, client: LlmClient, repository: StoryRepository):
        self.client = client
        self.repository = repository

    async def save_base_story(self, story_id: str, base_story: str):
        await self.repository.save_base_story(story_id, base_story)

    async def add_selected_content(self, story_id, selected_content: str):
        await self.repository.add_content(story_id, selected_content)

    # 동화 줄거리 요약
    async def summarize_story(self, story_id: str) -> str:
        story: Story = await self.repository.find_by_id(story_id)
        full_story = ', '.join(story.contents)
        prompt = self.get_story_summary_prompt(full_story)
        response = self.client.generate_response(prompt)
        return response['summary']

    # 동화 내용(페이지) 생성
    async def generate_content_options(self, story_id: str, page: int) -> List:
        story: Story = await self.repository.find_by_id(story_id)
        prompt = self.get_content_prompt(story, page)
        response = self.client.generate_response(prompt)
        return response['sentenceOptions']

    def get_content_prompt(self, story: Story, page: int):
        if page == 1:
            return self.get_first_content_prompt(story.base_story)
        return [
            {"role": "system", "content": "너는 동화의 다음 페이지를 생성하는 데에 능숙해."},
            {"role": "user", "content": f'''
                            아래 내용을 바탕으로 동화의 다음 페이지를 작성해줘. 
                            너는 총 10문단 중 {page}번째 문단을 작성해야 하고, 총 3개의 다음 문단 후보를 작성해줘.

                            base_story: """{story.base_story}"""\n
                            story_so_far: """{" ".join(story.contents)}"""\n

                            반드시 다음 JSON 형식으로만 응답해:
                            {{
                              "sentenceOptions": ["문장 후보1", "문장 후보2", "문장 후보3"],
                            }}
                            '''.strip()}
        ]

    def get_first_content_prompt(self, base_story: str):
        return [
            {"role": "system", "content": "너는 동화의 첫 페이지를 생성하는 데에 능숙해."},
            {"role": "user", "content": f'''
                            아래 내용을 바탕으로 동화의 첫 페이지를 작성해줘. 
                            총 3개의 다음 문단 후보를 작성해줘.

                            base_story: """{base_story}"""

                            반드시 다음 JSON 형식으로만 응답해:
                            {{
                              "sentenceOptions": ["문장 후보1", "문장 후보2", "문장 후보3"],
                            }}
                            '''.strip()}
        ]

    def get_story_summary_prompt(self, full_story: str):
        return [
            {"role": "system", "content": """너는 동화삽화 제작을 위해 한문장으로 내용을 영어로 요약해주는 AI야."""},
            {"role": "user", "content": f'''
                                동화 삽화 제작을 위해, 아래 문장을 한문장으로 요약해줘

                                story: """{full_story}"""

                                반드시 다음 JSON 형식으로만 응답해:
                                {{
                                    "summary": "삽화 제작을 위한 요약문"
                                }}
                                '''.strip()
             }
        ]
