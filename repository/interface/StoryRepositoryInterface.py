from abc import ABC, abstractmethod


class StoryRepositoryInterface(ABC):

    @abstractmethod
    def save_base_story(self, story_id: str, base_story: str):
        pass

    # @abstractmethod
    # def save_context(self, story_id: str, story_context: str):
    #     pass

    @abstractmethod
    def save_selected_sentence(self, story_id: str, selected_sentence: str):
        pass

    @abstractmethod
    async def find_story_by_id(self, story_id: str):
        pass

    @abstractmethod
    def find_by_id(self, story_id: str):
        pass

    @abstractmethod
    def delete_by_id(self, story_id: str):
        pass
