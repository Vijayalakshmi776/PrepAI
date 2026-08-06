from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssessmentAnswerBase(BaseModel):
    question_id: str
    user_id: str
    answer_text: str
    score: Optional[int] = None


class AssessmentAnswerCreate(AssessmentAnswerBase):
    pass


class AssessmentAnswerUpdate(BaseModel):
    answer_text: Optional[str] = None
    score: Optional[int] = None


class AssessmentAnswerRead(AssessmentAnswerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
