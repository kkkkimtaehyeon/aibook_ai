import json
import os
from utils.logConfig import logger
from dotenv import load_dotenv, find_dotenv
import requests
from openai import OpenAI

from repository.interface.StoryRepositoryInterface import StoryRepositoryInterface

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
IMAGE_GENERATION_BASE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

client = OpenAI(api_key=OPENAI_API_KEY)


class ImageGenerationServiceV2:
    def __init__(self, repository: StoryRepositoryInterface):
        self.repo = repository

    async def generate_image(self, story_id: str):
        # repo(redis)에서 story를 가져온다.
        story = await self.repo.find_story_by_id(story_id)
        # story contents로 이미지 생성 프롬프르틀 생성한다.
        cover_image_prompt = self.get_cover_image_prompt(story.contents)
        logger.debug(f"cover image prompt: {cover_image_prompt}")
        # 이미지 생성 프롬프트로 이미지를 생성한다.

        response = self.request_image_generation(cover_image_prompt["summary"])
        # json string을 dict로 변환
        response_dict = json.loads(response)
        # 응답에서 image만 추출해 반환
        return response_dict["image"]

    def request_image_generation(self, prompt: str):
        response = requests.post(
            IMAGE_GENERATION_BASE_URL,
            headers={
                "authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "application/json",
            },
            files={"none": ''},
            data={
                "prompt": "fairytale cover, for children, the summary of the story : " + prompt,
                "aspect_ratio": "1:1"
            },
        )

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(str(response.json()))

    def get_cover_image_prompt(self, contents: list[str]):
        prompt = self.get_image_generation_prompt(contents)
        return self.generate_response(prompt)

    def generate_response(self, messages: list):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            messages=messages
        )
        # JSON 응답 파싱
        return json.loads(response.choices[0].message.content)

    def get_image_generation_prompt(self, contents: list[str]):
        full_story = ", ".join(contents)
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
