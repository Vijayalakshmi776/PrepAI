from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class InterviewRound(Base, TimestampMixin):
    __tablename__ = 'interview_rounds'
    __table_args__ = (
        UniqueConstraint('pattern_id', 'order', name='uq_round_order'),
    )

    pattern_id = Column(ForeignKey('company_interview_patterns.id', ondelete='CASCADE'), nullable=False, index=True)
    order = Column(Integer, nullable=False)
    title = Column(String(128), nullable=False, index=True)
    description = Column(String(256), nullable=True)

    pattern = relationship('CompanyInterviewPattern', back_populates='rounds')
    interview_questions = relationship('InterviewQuestion', back_populates='round', cascade='all, delete-orphan')
