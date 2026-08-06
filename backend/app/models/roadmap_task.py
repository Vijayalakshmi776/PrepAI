from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class RoadmapTask(Base, TimestampMixin):
    __tablename__ = 'roadmap_tasks'

    roadmap_id = Column(ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
    priority = Column(Integer, nullable=False, default=0)
    due_date = Column(String(32), nullable=True)

    roadmap = relationship('Roadmap', back_populates='tasks')
