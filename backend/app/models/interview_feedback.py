from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class InterviewFeedback(Base, TimestampMixin):
    __tablename__ = 'interview_feedback'

    session_id = Column(ForeignKey('interview_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    summary = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)

    session = relationship('InterviewSession', back_populates='feedback')
