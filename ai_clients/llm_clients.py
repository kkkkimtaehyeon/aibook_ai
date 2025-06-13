import json
from abc import ABC, abstractmethod

from openai import OpenAI


class LlmClient(ABC):
    @abstractmethod
    def generate_response(self, prompt: str | list):
        pass


class GptLlmClient(LlmClient):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, prompt) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            response_format={"type": "json_object"},
            messages=prompt
        )
        # JSON 응답 파싱
        return json.loads(response.choices[0].message.content)
