from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Assessment(Base, TimestampMixin):
    __tablename__ = 'assessments'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship('User', back_populates='assessments')
    questions = relationship('AssessmentQuestion', back_populates='assessment', cascade='all, delete-orphan')
    results = relationship('AssessmentResult', back_populates='assessment', cascade='all, delete-orphan')
