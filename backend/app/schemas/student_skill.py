from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentSkillBase(BaseModel):
    user_id: str
    profile_id: str
    skill_id: str
    proficiency: Optional[int] = 0


class StudentSkillCreate(StudentSkillBase):
    pass


class StudentSkillUpdate(BaseModel):
    proficiency: Optional[int] = None


class StudentSkillRead(StudentSkillBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
