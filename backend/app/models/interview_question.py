from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class InterviewQuestion(Base, TimestampMixin):
    __tablename__ = 'interview_questions'

    session_id = Column(ForeignKey('interview_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    round_id = Column(ForeignKey('interview_rounds.id', ondelete='SET NULL'), nullable=True, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='SET NULL'), nullable=True, index=True)
    prompt = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False, default='text')
    options = Column(JSON, nullable=True)
    correct_answer = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)

    session = relationship('InterviewSession', back_populates='questions')
    round = relationship('InterviewRound', back_populates='interview_questions')
    skill = relationship('Skill', back_populates='interview_questions')
    answers = relationship('InterviewAnswer', back_populates='question', cascade='all, delete-orphan')
