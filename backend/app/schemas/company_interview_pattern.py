from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyInterviewPatternBase(BaseModel):
    company_id: str
    name: str
    description: Optional[str] = None


class CompanyInterviewPatternCreate(CompanyInterviewPatternBase):
    pass


class CompanyInterviewPatternUpdate(BaseModel):
    company_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class CompanyInterviewPatternRead(CompanyInterviewPatternBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
