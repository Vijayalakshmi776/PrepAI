from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssessmentQuestionBase(BaseModel):
    assessment_id: str
    skill_id: Optional[str] = None
    prompt: str
    weight: Optional[int] = 1


class AssessmentQuestionCreate(AssessmentQuestionBase):
    pass


class AssessmentQuestionUpdate(BaseModel):
    skill_id: Optional[str] = None
    prompt: Optional[str] = None
    weight: Optional[int] = None


class AssessmentQuestionRead(AssessmentQuestionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
