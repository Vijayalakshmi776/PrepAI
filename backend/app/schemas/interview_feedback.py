from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InterviewFeedbackBase(BaseModel):
    session_id: str
    summary: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    recommendations: Optional[str] = None


class InterviewFeedbackCreate(InterviewFeedbackBase):
    pass


class InterviewFeedbackUpdate(BaseModel):
    summary: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    recommendations: Optional[str] = None


class InterviewFeedbackRead(InterviewFeedbackBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
