from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Skill(Base, TimestampMixin):
    __tablename__ = 'skills'

    name = Column(String(128), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    student_skills = relationship('StudentSkill', back_populates='skill', cascade='all, delete-orphan')
    assessment_questions = relationship('AssessmentQuestion', back_populates='skill')
    interview_questions = relationship('InterviewQuestion', back_populates='skill')
    question_bank = relationship('QuestionBank', back_populates='skill')
