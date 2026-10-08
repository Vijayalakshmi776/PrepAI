from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class StudentProfile(Base, TimestampMixin):
    __tablename__ = 'student_profiles'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    headline = Column(String(256), nullable=True)
    biography = Column(Text, nullable=True)
    target_company_id = Column(ForeignKey('companies.id', ondelete='SET NULL'), nullable=True, index=True)
    target_role = Column(String(128), nullable=True)
    target_company = Column(String(128), nullable=True)
    current_level = Column(String(64), nullable=True)
    interview_difficulty = Column(String(64), nullable=True, default='Medium')
    career_goal = Column(String(128), nullable=True)

    user = relationship('User', back_populates='profile')
    target_company_ref = relationship('Company', foreign_keys=[target_company_id])
    skills = relationship('StudentSkill', back_populates='profile', cascade='all, delete-orphan')
    roadmap = relationship('Roadmap', back_populates='profile', uselist=False)
