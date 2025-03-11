import base64

from fastapi import APIRouter
import os
from dotenv import find_dotenv, load_dotenv

from modules.Zyphra import Zyphra
from schemas.schemas import VoiceCloningRequest, VoiceCloningResponse

_ = load_dotenv(find_dotenv())

router = APIRouter()

api_key = os.getenv("ZYPHRA_API_KEY")


@router.post('/api/voice-cloning')
async def voice_cloning(request: VoiceCloningRequest):
    zyphra = Zyphra(api_key)
    base64_audio = zyphra.get_base64_audio(request.audio_url)

    story_dubbing_dict = {}
    for page_id, content in request.story_page_map.items():
        audio_bytes: bytes = zyphra.generate_speech(base64_audio, content)
        story_dubbing_dict[page_id] = base64.b64encode(audio_bytes).decode('utf-8')
    # first_key, first_value = next(iter(request.story_page_map.items()))
    # audio_bytes: bytes = zyphra.generate_speech(base64_audio, first_value)
    # story_dubbing_dict[first_key] = base64.b64encode(audio_bytes).decode('utf-8')
    return VoiceCloningResponse(storyDubbingMap=story_dubbing_dict)
