from typing import Dict, Optional

from pydantic import BaseModel, Field


class StoryGenerateRequestOld(BaseModel):
    selected_content: str = Field(..., alias='selectedContent')
    # source: str = Field(..., alias='source')

    page_number: int = Field(..., alias='pageNumber')


class StoryGenerateResponseOld(BaseModel):
    content_option_1: str = Field(..., alias='contentOption1')
    content_option_2: str = Field(..., alias='contentOption2')
    content_option_3: str = Field(..., alias='contentOption3')


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


class StoryInitializationRequest(BaseModel):
    base_story: str = Field(..., alias='baseStory')


class StoryInitRequest(BaseModel):
    base_story: str = Field(..., alias="baseStory")


class StoryGenerateRequest(BaseModel):
    selected_sentence: str = Field(..., alias="selectedSentence")


class StoryGenerateRequestV2(BaseModel):
    base_story: Optional[str] = Field(default=None, alias="baseStory")
    selected_sentence: Optional[str] = Field(default=None, alias="selectedSentence")


class StoryGenerateResponse(BaseModel):
    sentence_options: list = Field(..., alias="sentenceOptions")


class ImageGenerationRequest(BaseModel):
    contents: list[str] = Field(...)
