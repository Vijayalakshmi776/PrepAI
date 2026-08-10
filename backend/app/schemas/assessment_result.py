from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AssessmentResultBase(BaseModel):
    assessment_id: str
    user_id: str
    total_score: Optional[float] = 0.0
    max_score: Optional[float] = 0.0
    percentile: Optional[float] = None
    status: Optional[str] = None


class AssessmentResultCreate(AssessmentResultBase):
    pass


class AssessmentResultUpdate(BaseModel):
    total_score: Optional[float] = None
    max_score: Optional[float] = None
    percentile: Optional[float] = None
    status: Optional[str] = None


class AssessmentResultRead(AssessmentResultBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
