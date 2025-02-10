from pydantic import BaseModel, Field


class StoryGenerateRequest(BaseModel):
    source: str = Field(..., alias='source')
    page_number: int = Field(..., alias='pageNumber')


class StoryGenerateResponse(BaseModel):
    content_option_1: str = Field(..., alias='contentOption1')
    content_option_2: str = Field(..., alias='contentOption2')
    content_option_3: str = Field(..., alias='contentOption3')
