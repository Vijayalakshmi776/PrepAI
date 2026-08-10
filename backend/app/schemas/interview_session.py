from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InterviewSessionBase(BaseModel):
    user_id: str
    company_id: Optional[str] = None
    pattern_id: Optional[str] = None
    title: str
    completed: Optional[bool] = False


class InterviewSessionCreate(InterviewSessionBase):
    pass


class InterviewSessionUpdate(BaseModel):
    company_id: Optional[str] = None
    pattern_id: Optional[str] = None
    title: Optional[str] = None
    completed: Optional[bool] = None


class InterviewSessionRead(InterviewSessionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
