from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SkillRead(SkillBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
