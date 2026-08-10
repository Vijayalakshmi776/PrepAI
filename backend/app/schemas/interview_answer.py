from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InterviewAnswerBase(BaseModel):
    question_id: str
    user_id: str
    response: str
    score: Optional[int] = None


class InterviewAnswerCreate(InterviewAnswerBase):
    pass


class InterviewAnswerUpdate(BaseModel):
    response: Optional[str] = None
    score: Optional[int] = None


class InterviewAnswerRead(InterviewAnswerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
