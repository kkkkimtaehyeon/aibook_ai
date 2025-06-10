import json

from openai import OpenAI

from repository.interface.StoryRepositoryInterface import StoryRepositoryInterface
from schemas.schemas import StoryInitRequest, StoryGenerateRequest, StoryGenerateResponse
from service.StoryGenerationServiceV2 import TempStory
from service.interface.StoryGenerationServiceInterface import StoryGenerationServiceInterface, Story


class StoryGenerationService(StoryGenerationServiceInterface):
    SYSTEM_ROLE = (
        "너는 동화작가의 조수로, 동화작가를 도와서 발단, 전개, 절정, 결말을 가지는 구조의 글을 작성해. 7살짜리 아이를 위한 총 10페이지의 동화를 작성하게 될거야"
    )

    def __init__(self, client: OpenAI, repository: StoryRepositoryInterface):
        self.client = client
        self.repository = repository

    # gpt에 답변 생성 요청
    def _generate_response(self, messages: list):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            response_format={"type": "json_object"},
            messages=messages
        )
        # JSON 응답 파싱
        return json.loads(response.choices[0].message.content)


    def generate_first_story(self, story_id: str, request: StoryInitRequest) -> StoryGenerateResponse:
        base_story = request.base_story
        self.repository.save_base_story(story_id, base_story)
        sentence_options = self._generate_sentences_for_page(base_story, 1)

    # 변경 전: 동화 첫 페이지 문장 후보 생성
    # def generate_first_story(self, story_id: str, request: StoryInitRequest) -> StoryGenerateResponse:
    #     story = self._init_story_context(story_id, request.base_story)
    #     sentence_options = self._generate_sentences_for_page(story, 1)
    #     return StoryGenerateResponse(sentenceOptions=sentence_options)

    def generate_story(self, story_id: str, page_number: int, request: StoryGenerateRequest) -> StoryGenerateResponse:
        story = self.repository.save_selected_sentence(story_id, request.selected_sentence)
        sentence_options = self._generate_sentences_for_page(story, page_number + 1)
        return StoryGenerateResponse(sentenceOptions=sentence_options)

    def generate_image_generation_prompt(self, story: TempStory) -> str:
        source = ', '.join(story.contents)
        messages = self.get_image_generation_prompt(source)
        response = self._generate_response(messages)
        return response["prompt"]

    # base_story에서 story_context를 추출하고 반환
    def _init_story_context(self, story_id: str, base_story: str) -> Story:
        messages = self._get_story_context_prompt(base_story)
        story_context = self._generate_response(messages)
        story = self.repository.save_context(story_id, story_context)
        return story

    # story_id에 해당하는 스토리에서 page_number에 대한 문장 후보 3개를 생성
    def _generate_sentences_for_page(self, story: Story, page_number: int) -> list:
        messages = self._get_story_generating_prompt(story, page_number)
        sentences = self._generate_response(messages)["sentenceOptions"]
        return sentences

    def get_image_generation_prompt(self, source: str):
        return [
            {"role": "system", "content": f"너는 이미지 생성 프롬프트를 작성하는 데에 능숙해."},
            {"role": "user", "content": f'''
                    아래 내용을 바탕으로 이미지 생성 프롬프트를 작성해줘.  
                    반드시 영어로 작성하고, **구체적이고 간결하게** 작성해.  
        
                    source: """{source}"""
        
                    반드시 영어로 다음 json 형식으로만 응답해:
                    {{
                      "prompt": "image generation prompt"
                    }}
                    '''.strip()}
        ]

    # story_context를 추출하는 프롬프트
    def _get_story_context_prompt(self, base_story: str):
        return [
            {"role": "system", "content": f"{self.SYSTEM_ROLE} 핵심만 뽑아내는 데에 능숙해."},
            {"role": "user", "content": f'''
                    base_story를 분석해서 동화 제작에 꼭 필요한 최소한의 핵심 정보를 아래 JSON 형식에 맞춰 추출해줘.  
                    가능한 한 **구체적이고 간결하게** 작성해.  
        
                    base_story: """{base_story}"""
        
                    반드시 다음 JSON 형식으로만 응답해:
                    {{
                      "characters": ["등장인물1", "등장인물2"],
                      "setting": "시간과 장소 포함한 배경 설명",
                      "mainTheme": "이야기의 중심 주제",
                      "keyEvents": ["핵심 사건1", "핵심 사건2", ...]
                    }}
                    '''.strip()}
        ]

    def _get_story_generating_prompt(self, story: Story, page_number: int):
        return [
            {"role": "system", "content": self.SYSTEM_ROLE},
            {"role": "user", "content": f'''
                    아래 정보를 바탕으로, 총 3개의 다음 문단 후보를 만들어줘. 

                    story_context: """{story.get_context()}"""
                    current_page: """{page_number} / 10 """
                    story_history: """{", ".join(story.get_sentences())}"""
                    story_arc: """{self._get_story_arc(page_number)}"""

                    반드시 다음 JSON 형식으로만 응답해:
                    {{
                      "sentenceOptions": ["문장 후보1", "문장 후보2", "문장 후보3"],
                    }}
                    '''.strip()}
        ]

    def _get_story_arc(self, page_number: int) -> str:
        if page_number == 1:
            return "발단"
        elif page_number <= 5:
            return "전개"
        elif page_number <= 8:
            return "절정"
        else:
            return "결말"
