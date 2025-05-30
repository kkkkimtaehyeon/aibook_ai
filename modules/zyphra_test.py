import asyncio
import base64
import os
import time

from dotenv import find_dotenv, load_dotenv
import requests
from zyphra import AsyncZyphraClient
_ = load_dotenv(find_dotenv())
api_key = os.getenv("ZYPHRA_API_KEY")


async def zyphra(audio_url):
    audio_file = requests.get(audio_url).content
    base64_audio = base64.b64encode(audio_file).decode('utf-8')
    start = time.time()
    async with AsyncZyphraClient(api_key=api_key) as client:
        audio_data = await client.audio.speech.create(
            text="안녕하세요. 테스트입니다.",
            language_iso_code='ko',
            speaking_rate=15,
            speaker_audio=base64_audio,
            mime_type="audio/wav",
            model="zonos-v0.1-transformer",
        )
    with open(f"tts_sample_{start}.wav", "wb") as f:
        f.write(audio_data)
    end = time.time()
    print(f"tts process ended!: {end - start} ms")


asyncio.run(zyphra("https://aibook-bucket.s3.ap-northeast-2.amazonaws.com/recording4b4aabe4-569d-4fc4-95ef-b00118f02804.wav"))