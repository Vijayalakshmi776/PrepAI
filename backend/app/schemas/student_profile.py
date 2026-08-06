from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StudentProfileBase(BaseModel):
    headline: Optional[str] = None
    biography: Optional[str] = None
    target_company_id: Optional[str] = None
    target_role: Optional[str] = None
    target_company: Optional[str] = None
    current_level: Optional[str] = None
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
    career_goal: Optional[str] = None


class StudentProfileRead(StudentProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
