from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class SkillGap(Base, TimestampMixin):
    __tablename__ = 'skill_gaps'
    __table_args__ = (
        UniqueConstraint('user_id', 'skill_id', name='uq_user_skill_gap'),
    )

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    skill_id = Column(ForeignKey('skills.id', ondelete='CASCADE'), nullable=False, index=True)
    gap_description = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=0)

    user = relationship('User')
    skill = relationship('Skill')
