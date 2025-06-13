import base64
from abc import ABC, abstractmethod
from google import genai
from google.genai import types


class ImageClient(ABC):
    @abstractmethod
    def generate_image(self, prompt: str) -> str:
        pass


class GeminiImageClient(ImageClient):
    def __init__(self, gemini_api_key: str):
        self.client = genai.Client(api_key=gemini_api_key)

    def generate_image(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                base64_img = base64.b64encode(part.inline_data.data).decode('utf-8')
                return base64_img
            else:
                raise ValueError("image generation failed, no inline data found")


class StableDiffusionImageClient(ImageClient):
    def generate_image(self, prompt: str) -> str:
        # Implementation for Gemini image generation
        pass
