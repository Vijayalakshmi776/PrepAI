from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class InterviewAnswer(Base, TimestampMixin):
    __tablename__ = 'interview_answers'

    question_id = Column(ForeignKey('interview_questions.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    response = Column(Text, nullable=False)
    score = Column(Integer, nullable=True)

    question = relationship('InterviewQuestion', back_populates='answers')
    user = relationship('User')
