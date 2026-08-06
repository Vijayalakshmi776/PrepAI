from sqlalchemy import Column, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class CompanyInterviewPattern(Base, TimestampMixin):
    __tablename__ = 'company_interview_patterns'
    __table_args__ = (
        UniqueConstraint('company_id', 'name', name='uq_company_pattern_name'),
    )

    company_id = Column(ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)

    company = relationship('Company', back_populates='interview_patterns')
    rounds = relationship('InterviewRound', back_populates='pattern', cascade='all, delete-orphan')
