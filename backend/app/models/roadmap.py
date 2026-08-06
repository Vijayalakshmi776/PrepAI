from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Roadmap(Base, TimestampMixin):
    __tablename__ = 'roadmaps'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    profile_id = Column(ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=True, index=True)
    title = Column(String(128), nullable=False)
    summary = Column(Text, nullable=True)

    user = relationship('User', back_populates='roadmap')
    profile = relationship('StudentProfile', back_populates='roadmap')
    tasks = relationship('RoadmapTask', back_populates='roadmap', cascade='all, delete-orphan')
