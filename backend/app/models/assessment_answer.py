from sqlalchemy import Column, String, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class AssessmentAnswer(Base, TimestampMixin):
    __tablename__ = 'assessment_answers'

    question_id = Column(ForeignKey('assessment_questions.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    response = Column(Text, nullable=False)
    score = Column(Integer, nullable=True)
    is_correct = Column(Boolean, nullable=True)

    question = relationship('AssessmentQuestion', back_populates='answers')
    user = relationship('User')
