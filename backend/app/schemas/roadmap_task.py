from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RoadmapTaskBase(BaseModel):
    roadmap_id: str
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[int] = 0
    due_date: Optional[str] = None


class RoadmapTaskCreate(RoadmapTaskBase):
    pass


class RoadmapTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None


class RoadmapTaskRead(RoadmapTaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
