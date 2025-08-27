from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"

class StoryRequest(BaseModel):
    character: Optional[str] = None
    theme: Optional[str] = None
    duration: int = 2
    language: Language = Language.ENGLISH

class StoryResponse(BaseModel):
    story: str
    duration: int
    language: str
    audio_url: Optional[str] = None

class NarrateRequest(BaseModel):
    text: str
    language: Language = Language.ENGLISH

class NarrateResponse(BaseModel):
    audio_url: str
    duration: float
