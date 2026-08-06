from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InterviewRoundBase(BaseModel):
    pattern_id: str
    order: int
    title: str
    description: Optional[str] = None


class InterviewRoundCreate(InterviewRoundBase):
    pass


class InterviewRoundUpdate(BaseModel):
    order: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None


class InterviewRoundRead(InterviewRoundBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
