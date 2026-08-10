from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AIConversationBase(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    topic: Optional[str] = None
    conversation_type: Optional[str] = None
    messages: Optional[str] = None
    metadata: Optional[str] = None
    status: Optional[str] = None


class AIConversationCreate(AIConversationBase):
    pass


class AIConversationUpdate(BaseModel):
    topic: Optional[str] = None
    conversation_type: Optional[str] = None
    messages: Optional[str] = None
    metadata: Optional[str] = None
    status: Optional[str] = None


class AIConversationRead(AIConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
