import os

from dotenv import find_dotenv, load_dotenv
from zyphra import ZyphraClient

_ = load_dotenv(find_dotenv())

# Initialize the client
client = ZyphraClient(api_key=os.getenv('ZYPHRA_API_KEY'))

# Generate speech and save to file
output_path = client.audio.speech.create(
    text="오늘은 날씨가 좋아서 산책을 갈거예요",
    language_iso_code="ko",
    speaking_rate=15,
    output_path="output.webm",
)


# # Or get audio data as bytes
# audio_data = client.audio.speech.create(
#     text="Hello, world!",
#     speaking_rate=15
# )
