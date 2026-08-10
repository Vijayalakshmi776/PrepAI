from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class QuestionBankBase(BaseModel):
    skill_id: Optional[str] = None
    question_text: str
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[str] = None


class QuestionBankCreate(QuestionBankBase):
    pass


class QuestionBankUpdate(BaseModel):
    skill_id: Optional[str] = None
    question_text: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[str] = None


class QuestionBankRead(QuestionBankBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
