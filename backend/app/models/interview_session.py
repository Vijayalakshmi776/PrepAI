from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class InterviewSession(Base, TimestampMixin):
    __tablename__ = 'interview_sessions'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    company_id = Column(ForeignKey('companies.id', ondelete='SET NULL'), nullable=True, index=True)
    pattern_id = Column(ForeignKey('company_interview_patterns.id', ondelete='SET NULL'), nullable=True, index=True)
    title = Column(String(128), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)

    user = relationship('User', back_populates='interview_sessions')
    company = relationship('Company')
    pattern = relationship('CompanyInterviewPattern')
    questions = relationship('InterviewQuestion', back_populates='session', cascade='all, delete-orphan')
    feedback = relationship('InterviewFeedback', back_populates='session', cascade='all, delete-orphan')
    ai_conversations = relationship('AIConversation', back_populates='session', cascade='all, delete-orphan')
