from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.sqlalchemy.connection import Base


class ChoiceModel(Base):
    __tablename__ = 'choices'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"), index=True)
    question_id = Column(UUID, ForeignKey('questions.id'), index=True)
    question = relationship("QuestionModel", back_populates="choices")
    answer = Column(String)
    is_correct = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
