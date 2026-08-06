from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class ResumeBase(BaseModel):
    user_id: str
    title: str
    content: Optional[str] = None
    file_type: Optional[str] = None
    language: Optional[str] = None
    word_count: Optional[int] = None
    keywords: Optional[str] = None
    source_url: Optional[HttpUrl] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    file_type: Optional[str] = None
    language: Optional[str] = None
    word_count: Optional[int] = None
    keywords: Optional[str] = None
    source_url: Optional[HttpUrl] = None


class ResumeRead(ResumeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
