from abc import ABC, abstractmethod


class ImageGenerationServiceInterface(ABC):

    @abstractmethod
    def generate_image(self, prompt: str):
        pass

    
