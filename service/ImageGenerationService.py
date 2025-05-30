import json
import os

import requests
from dotenv import find_dotenv, load_dotenv

from service.interface.ImageGenerationServiceInterface import ImageGenerationServiceInterface

_ = load_dotenv(find_dotenv())

api_key = os.getenv("STABILITY_API_KEY")


class ImageGenerationService(ImageGenerationServiceInterface):
    def __init__(self):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def generate_image(self, prompt: str):
        response = requests.post(
            self.base_url,
            headers={
                "authorization": f"Bearer {api_key}",
                "accept": "application/json",
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "aspect_ratio": "1:1"
            },
        )

        if response.status_code == 200:
            response_content: bytes = response.content
            json_response: dict = json.loads(response_content)
            return json_response["image"]
        else:
            raise Exception(str(response.json()))
