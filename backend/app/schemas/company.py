from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    company_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    logo_url: Optional[HttpUrl] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    company_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    logo_url: Optional[HttpUrl] = None


class CompanyRead(CompanyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
