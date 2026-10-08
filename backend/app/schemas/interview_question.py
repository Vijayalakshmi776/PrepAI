from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InterviewQuestionBase(BaseModel):
    session_id: str
    round_id: Optional[str] = None
    skill_id: Optional[str] = None
    prompt: str
    question_type: str = "text"
    options: Optional[list[str]] = None
    correct_answer: Optional[str] = None
    order: Optional[int] = 0


class InterviewQuestionCreate(InterviewQuestionBase):
    pass


class InterviewQuestionUpdate(BaseModel):
    round_id: Optional[str] = None
    skill_id: Optional[str] = None
    prompt: Optional[str] = None
    order: Optional[int] = None


class InterviewQuestionRead(InterviewQuestionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
