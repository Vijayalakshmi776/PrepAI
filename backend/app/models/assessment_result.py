from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class AssessmentResult(Base, TimestampMixin):
    __tablename__ = 'assessment_results'

    assessment_id = Column(ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    total_score = Column(Float, nullable=False, default=0.0)
    max_score = Column(Float, nullable=False, default=0.0)
    percentile = Column(Float, nullable=True)
    status = Column(String(64), nullable=True)

    assessment = relationship('Assessment', back_populates='results')
    user = relationship('User')
