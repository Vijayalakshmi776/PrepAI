from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RoadmapBase(BaseModel):
    user_id: str
    profile_id: Optional[str] = None
    title: str
    summary: Optional[str] = None


class RoadmapCreate(RoadmapBase):
    pass


class RoadmapUpdate(BaseModel):
    profile_id: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None


class RoadmapRead(RoadmapBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
