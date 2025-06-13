from typing import Dict, Optional, List

from pydantic import BaseModel, Field


class VoiceCloningRequest(BaseModel):
    audio_url: str = Field(..., alias='audioUrl')
    story_page_map: Dict[int, str] = Field(..., alias='storyPageMap')
    webhook_url: str = Field(..., alias='webhookUrl')


class DubbingContentAndPreSignedUrl(BaseModel):
    content: str = Field(..., alias='content')
    pre_signed_url: str = Field(..., alias='preSignedUrl')


class DubbingRequest(BaseModel):
    voice_audio_url: str = Field(..., alias='voiceAudioUrl')
    story_page_map: Dict[int, DubbingContentAndPreSignedUrl] = Field(..., alias='storyPageMap')
    webhook_url: str = Field(..., alias='webhookUrl')


class VoiceCloningResponse(BaseModel):
    story_dubbing_dict: Dict[int, str] = Field(..., alias='storyDubbingMap')


class StoryGenerateRequestV2(BaseModel):
    base_story: Optional[str] = Field(default=None, alias="baseStory")
    selected_sentence: Optional[str] = Field(default=None, alias="selectedSentence")


class StoryGenerateRequest(BaseModel):
    base_story: Optional[str] = Field(default=None, alias="baseStory")
    selected_sentence: Optional[str] = Field(default=None, alias="selectedSentence")


class Story(BaseModel):
    base_story: str
    contents: List[str] = []
