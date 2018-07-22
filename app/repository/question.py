import sqlalchemy
import logging
import pygogo as gogo

from typing import Dict

from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.sql import func

from app.model.question import QuestionModel
from app.model.choices import ChoiceModel
from app.model.lesson import LessonModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class QuestionRepository:

    def get(self, uuid: str, session=None) -> QuestionModel:
        logger.info("Get CourseRepository")
        lesson = session.query(QuestionModel).get(uuid)

        return lesson

    def get_all_active(self, lesson_id, session=None):
        logger.info("get_all_active QuestionRepository")
        questions = session.query(QuestionModel)\
            .filter(QuestionModel.lesson_id == lesson_id, QuestionModel.active).all()
        return questions

    def get_all_active_user(self, lesson_id, session=None):
        logger.info("get_all_active QuestionRepository")
        questions = session.query(QuestionModel)\
            .filter(QuestionModel.lesson_id == lesson_id, QuestionModel.active).all()
        return questions

    def save(self, data: Dict, lesson_id: str, user_id: str, session=None) -> QuestionModel:
        try:
            logger.info("save QuestionRepository")
            question = QuestionModel()
            corrects = data['corrects']
            wrong = data['wrong']
            question.question = data['question']
            question.code = data['code']
            question.score = data['score']
            question.lesson_id = lesson_id
            question.type_question = data['type_question']
            question.created_by = user_id
            question.active = True

            for c in corrects:
                choice = ChoiceModel()
                choice.answer = c['answer']
                choice.is_correct = True
                question.choices.append(choice)
                session.add(choice)

            for w in wrong:
                choice = ChoiceModel()
                choice.answer = w['answer']
                choice.is_correct = False
                question.choices.append(choice)
                session.add(choice)

            session.add(question)
            total_score = session.query(
                func.sum(QuestionModel.score).label("total_score"),
                                ).filter(QuestionModel.lesson_id == lesson_id).scalar()
            #total_score, total_rows = session.execute(query).first()
            print(question.score)
            print(total_score)
            #total_score += question.score
            session.query(LessonModel).filter(LessonModel.id == lesson_id)\
                .update({"score": total_score})
            session.commit()

            return question
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("La pregunta no se ha podido dar de alta.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

    def get_correct_answers(self, lesson_id, session):
        try:
            logger.info("save LessonRepository")
            #answers_agg = func.array_agg(ChoiceModel.id, type_=ARRAY(UUID)).label('answers')
            q = QuestionModel.get_correct_answers(lesson_id, session)
            return q
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("El nombre o código del curso ya existe.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc