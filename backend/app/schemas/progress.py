from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProgressBase(BaseModel):
    user_id: str
    category: str
    completed_count: Optional[int] = 0
    score: Optional[float] = None
    xp_points: Optional[int] = 0
    streak_days: Optional[int] = 0
    last_activity: Optional[datetime] = None


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    category: Optional[str] = None
    completed_count: Optional[int] = None
    score: Optional[float] = None
    xp_points: Optional[int] = None
    streak_days: Optional[int] = None
    last_activity: Optional[datetime] = None


class ProgressRead(ProgressBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
