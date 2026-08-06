from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class InterviewQuestion(Base, TimestampMixin):
    __tablename__ = 'interview_questions'

    session_id = Column(ForeignKey('interview_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    round_id = Column(ForeignKey('interview_rounds.id', ondelete='SET NULL'), nullable=True, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='SET NULL'), nullable=True, index=True)
    prompt = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)

    session = relationship('InterviewSession', back_populates='questions')
    round = relationship('InterviewRound', back_populates='interview_questions')
    skill = relationship('Skill', back_populates='interview_questions')
    answers = relationship('InterviewAnswer', back_populates='question', cascade='all, delete-orphan')
