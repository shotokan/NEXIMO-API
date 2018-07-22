import uuid

import sqlalchemy

from sqlalchemy import Column, DateTime, func, ForeignKey, Boolean, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.sqlalchemy.connection import Base


class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    id = Column(UUID, primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    user_id = Column('user_id', UUID, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="enrollments")
    course_id = Column('course_id', UUID, ForeignKey('courses.id'))
    course = relationship("CourseModel", back_populates="users")
    lesson_scores = relationship("LessonScoreModel", back_populates="enrollment")
    date_of_enrollment = Column(DateTime, default=func.now())
    date_of_completation = Column(DateTime)
    total_score = Column(Float)
    status = Column(String(20))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())