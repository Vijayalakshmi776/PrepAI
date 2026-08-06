from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class AIConversation(Base, TimestampMixin):
    __tablename__ = 'ai_conversations'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_id = Column(ForeignKey('interview_sessions.id', ondelete='SET NULL'), nullable=True, index=True)
    topic = Column(String(128), nullable=True)
    conversation_type = Column(String(64), nullable=True)
    messages = Column(Text, nullable=True)
    metadata = Column(Text, nullable=True)
    status = Column(String(64), nullable=True)

    user = relationship('User', back_populates='ai_conversations')
    session = relationship('InterviewSession', back_populates='ai_conversations')
