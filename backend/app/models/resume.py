from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Resume(Base, TimestampMixin):
    __tablename__ = 'resumes'

    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=True)
    file_type = Column(String(32), nullable=True)
    language = Column(String(32), nullable=True)
    word_count = Column(Integer, nullable=True)
    keywords = Column(String(256), nullable=True)
    source_url = Column(String(256), nullable=True)

    user = relationship('User', back_populates='resumes')
    analyses = relationship('ResumeAnalysis', back_populates='resume', cascade='all, delete-orphan')
