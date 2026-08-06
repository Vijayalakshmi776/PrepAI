from sqlalchemy import Column, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class ResumeAnalysis(Base, TimestampMixin):
    __tablename__ = 'resume_analyses'

    resume_id = Column(ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False, index=True)
    readiness_score = Column(Float, nullable=True)
    clarity_score = Column(Float, nullable=True)
    impact_score = Column(Float, nullable=True)
    skill_alignment_score = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    skill_gaps = Column(Text, nullable=True)

    resume = relationship('Resume', back_populates='analyses')
