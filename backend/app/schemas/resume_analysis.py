from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResumeAnalysisBase(BaseModel):
    resume_id: str
    readiness_score: Optional[float] = None
    clarity_score: Optional[float] = None
    impact_score: Optional[float] = None
    skill_alignment_score: Optional[float] = None
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    skill_gaps: Optional[str] = None


class ResumeAnalysisCreate(ResumeAnalysisBase):
    pass


class ResumeAnalysisUpdate(BaseModel):
    readiness_score: Optional[float] = None
    clarity_score: Optional[float] = None
    impact_score: Optional[float] = None
    skill_alignment_score: Optional[float] = None
    summary: Optional[str] = None
    recommendations: Optional[str] = None
    skill_gaps: Optional[str] = None


class ResumeAnalysisRead(ResumeAnalysisBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
