from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.sqlalchemy.connection import Base
from app.model.choices import ChoiceModel


class QuestionModel(Base):
    __tablename__ = 'questions'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"), index=True)
    question = Column(String)
    code = Column(String)
    score = Column(Integer)
    lesson_id = Column(UUID, ForeignKey('lessons.id'), index=True)
    lesson = relationship("LessonModel", back_populates="questions")
    type_question = Column(String)
    created_by = Column(UUID)
    active = Column(Boolean, default=True)
    answers = Column(ARRAY(String))
    choices = relationship("ChoiceModel", back_populates="question")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    @classmethod
    def get_correct_answers(cls, lesson_id, session):
        answers_agg = func.array_agg(ChoiceModel.id, type_=ARRAY(UUID)).label('answers')
        return session.query(ChoiceModel.question_id, QuestionModel.score, QuestionModel.type_question, answers_agg). \
                join(QuestionModel.choices) \
                .filter(QuestionModel.lesson_id == lesson_id, ChoiceModel.is_correct) \
                .group_by(ChoiceModel.question_id).group_by(QuestionModel.score) \
                .group_by(QuestionModel.type_question)\
                .all()
