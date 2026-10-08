from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StudentProfileBase(BaseModel):
    headline: Optional[str] = None
    biography: Optional[str] = None
    target_company_id: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    current_level: Optional[str] = None
    interview_difficulty: Optional[str] = 'Medium'
    career_goal: Optional[str] = None


class StudentProfileCreate(StudentProfileBase):
    user_id: str


class StudentProfileUpdate(BaseModel):
    headline: Optional[str] = None
    biography: Optional[str] = None
    target_company_id: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    current_level: Optional[str] = None
    interview_difficulty: Optional[str] = 'Medium'
    career_goal: Optional[str] = None


class StudentProfileRead(StudentProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
