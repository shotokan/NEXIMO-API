from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.sqlalchemy.connection import Base


class LessonScoreModel(Base):
    __tablename__ = 'lesson_scores'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    enrollment_id = Column(UUID, ForeignKey('enrollments.id'))
    lesson_id = Column(UUID, ForeignKey('lessons.id'))
    enrollment = relationship("EnrollmentModel", back_populates="lesson_scores")
    lesson_result = Column(Float)
    successful_answers = Column(Integer)
    unsuccessful_answers = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
