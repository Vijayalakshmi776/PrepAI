from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class StudentSkill(Base, TimestampMixin):
    __tablename__ = 'student_skills'
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_id', name='uq_user_skill'),
    )

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    profile_id = Column(ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='CASCADE'), nullable=False, index=True)
    proficiency = Column(Integer, nullable=False, default=0)

    user = relationship('User', back_populates='skills')
    profile = relationship('StudentProfile', back_populates='skills')
    skill = relationship('Skill', back_populates='student_skills')
