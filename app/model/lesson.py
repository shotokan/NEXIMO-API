from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.sqlalchemy.connection import Base


class LessonModel(Base):
    __tablename__ = 'lessons'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String)
    description = Column(String)
    question_details = Column(String)
    code = Column(String)
    order = Column(Integer, autoincrement=True)
    hours = Column(Integer)
    score = Column(Integer, default=1)
    course_id = Column(UUID, ForeignKey('courses.id'))
    course = relationship("CourseModel", back_populates="lessons")
    created_by = Column(UUID)
    updated_by = Column(UUID)
    questions = relationship("QuestionModel", back_populates="lesson")
    active = Column(Boolean, default=True)
    aproval_score = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
