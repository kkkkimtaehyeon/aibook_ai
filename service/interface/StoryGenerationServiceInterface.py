from abc import ABC, abstractmethod

from schemas.schemas import StoryGenerateResponse, StoryInitRequest, StoryGenerateRequest


class StoryGenerationServiceInterface(ABC):

    # @abstractmethod
    # def generate_story_content(self, story_id: str, ):
    #     pass

    @abstractmethod
    def generate_first_story(self, story_id: str, request: StoryInitRequest) -> StoryGenerateResponse:
        pass

    @abstractmethod
    def generate_story(self, story_id: str, page_number: int, request: StoryGenerateRequest) -> StoryGenerateResponse:
        pass

    @abstractmethod
    def generate_image_generation_prompt(self, source: str) -> str:
        pass


class Story:
    def __init__(self, base_story: str):
        self.base_story = base_story
        self.sentences = []

    # def __init__(self, story_context: str):
    #     self.context = story_context
    #     self.sentences = []

    def set_context(self, context: str):
        self.context = context

    def add_sentence(self, sentence: str):
        self.sentences.append(sentence)

    def get_context(self):
        return self.context

    def get_sentences(self):
        return self.sentences
