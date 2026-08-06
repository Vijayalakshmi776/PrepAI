from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class AssessmentQuestion(Base, TimestampMixin):
    __tablename__ = 'assessment_questions'

    assessment_id = Column(ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='SET NULL'), nullable=True, index=True)
    prompt = Column(Text, nullable=False)
    weight = Column(Integer, nullable=False, default=1)

    assessment = relationship('Assessment', back_populates='questions')
    skill = relationship('Skill', back_populates='assessment_questions')
    answers = relationship('AssessmentAnswer', back_populates='question', cascade='all, delete-orphan')
