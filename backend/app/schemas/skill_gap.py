from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SkillGapBase(BaseModel):
    user_id: str
    skill_id: str
    gap_description: Optional[str] = None
    priority: Optional[int] = 0


class SkillGapCreate(SkillGapBase):
    pass


class SkillGapUpdate(BaseModel):
    gap_description: Optional[str] = None
    priority: Optional[int] = None


class SkillGapRead(SkillGapBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
