import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    email = Column(String(256), unique=True, nullable=False, index=True)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(128), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)

    profile = relationship('StudentProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    assessments = relationship('Assessment', back_populates='user', cascade='all, delete-orphan')
    interview_sessions = relationship('InterviewSession', back_populates='user', cascade='all, delete-orphan')
    resumes = relationship('Resume', back_populates='user', cascade='all, delete-orphan')
    roadmap = relationship('Roadmap', back_populates='user', uselist=False, cascade='all, delete-orphan')
    progress_entries = relationship('Progress', back_populates='user', cascade='all, delete-orphan')
    skills = relationship('StudentSkill', back_populates='user', cascade='all, delete-orphan')
    ai_conversations = relationship('AIConversation', back_populates='user', cascade='all, delete-orphan')
