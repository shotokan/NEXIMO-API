from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, ARRAY, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.sqlalchemy.connection import Base


class CourseModel(Base):
    __tablename__ = 'courses'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, unique=True)
    description = Column(String)
    code = Column(String, unique=True)
    mandatory_courses = Column(ARRAY(UUID), default=None)
    mandatory_courses_code = Column(ARRAY(String), default=None)
    credits = Column(Integer)
    created_by = Column(UUID)
    updated_by = Column(UUID)
    approval_score = Column(Float)
    active = Column(Boolean, default=True)
    lessons = relationship("LessonModel", back_populates="course")
    users = relationship("EnrollmentModel", back_populates="course")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
