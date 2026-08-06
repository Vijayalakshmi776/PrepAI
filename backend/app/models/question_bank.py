from sqlalchemy import Column, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class QuestionBank(Base, TimestampMixin):
    __tablename__ = 'question_bank'
    __table_args__ = (
        UniqueConstraint('skill_id', 'question_text', name='uq_question_bank_skill_question'),
    )

    skill_id = Column(ForeignKey('skills.id', ondelete='SET NULL'), nullable=True, index=True)
    question_text = Column(Text, nullable=False)
    category = Column(String(128), nullable=True)
    difficulty_level = Column(String(64), nullable=True)
    source = Column(String(128), nullable=True)
    tags = Column(String(256), nullable=True)

    skill = relationship('Skill', back_populates='question_bank')
