from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Progress(Base, TimestampMixin):
    __tablename__ = 'progress_entries'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    category = Column(String(128), nullable=False)
    completed_count = Column(Integer, nullable=False, default=0)
    score = Column(Float, nullable=True)
    xp_points = Column(Integer, nullable=False, default=0)
    streak_days = Column(Integer, nullable=False, default=0)
    last_activity = Column(DateTime(timezone=True), nullable=True)

    user = relationship('User', back_populates='progress_entries')
