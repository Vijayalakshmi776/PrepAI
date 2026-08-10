from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AssessmentBase(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AssessmentRead(AssessmentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
