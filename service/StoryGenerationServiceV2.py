import json
import os
from typing import Optional

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

from repository.interface.StoryRepositoryInterface import StoryRepositoryInterface

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)


class TempStory:
    def __init__(self, base_story: str, contents: Optional[list[str]] = None):
        self.base_story = base_story
        self.contents = contents if contents is not None else []

    def add_content(self, content: str):
        self.contents.append(content)

    def to_dict(self):
        return {
            "base_story": self.base_story,
            "contents": self.contents
        }

    @classmethod
    def from_dict(cls, story_dict: dict):
        return cls(
            base_story=story_dict["base_story"],
            contents=story_dict["contents"]
        )


class StoryGenerationServiceV2:
    def __init__(self, repository: StoryRepositoryInterface):
        self.repo = repository
        # self.repo = {}

    async def set_base_story(self, story_id: str, base_story: str):
        story = await self.repo.save_base_story(story_id, base_story)
        return story

    async def add_content(self, story_id: str, content: str):
        return await self.repo.save_selected_sentence(story_id, content)

    def generate_content(self, story: TempStory, page_number: int):
        prompt = self.get_page_prompt(story, page_number)
        response = self._generate_response(prompt)
        return response

    def _generate_response(self, messages: list):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            response_format={"type": "json_object"},
            messages=messages
        )
        # JSON 응답 파싱
        return json.loads(response.choices[0].message.content)

    def get_first_page_prompt(self, base_story: str):
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

    def get_page_prompt(self, temp_story: TempStory, page_number: int):
        if page_number == 1:
            return self.get_first_page_prompt(temp_story.base_story)
        return [
            {"role": "system", "content": "너는 동화의 다음 페이지를 생성하는 데에 능숙해."},
            {"role": "user", "content": f'''
                    아래 내용을 바탕으로 동화의 다음 페이지를 작성해줘. 
                    너는 총 10문단 중 {page_number}번째 문단을 작성해야 하고, 총 3개의 다음 문단 후보를 작성해줘.

                    base_story: """{temp_story.base_story}"""\n
                    story_so_far: """{" ".join(temp_story.contents)}"""\n

                    반드시 다음 JSON 형식으로만 응답해:
                    {{
                      "sentenceOptions": ["문장 후보1", "문장 후보2", "문장 후보3"],
                    }}
                    '''.strip()}
        ]
