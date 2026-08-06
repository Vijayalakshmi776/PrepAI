from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = 'companies'

    name = Column(String(128), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    website = Column(String(256), nullable=True)
    company_type = Column(String(64), nullable=True)
    difficulty_level = Column(String(64), nullable=True)
    logo_url = Column(String(256), nullable=True)

    interview_patterns = relationship('CompanyInterviewPattern', back_populates='company', cascade='all, delete-orphan')
