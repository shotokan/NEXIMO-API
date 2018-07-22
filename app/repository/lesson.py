import sqlalchemy
import logging
import pygogo as gogo

from typing import Dict

from app.model.lesson import LessonModel
from app.model.enrollment import EnrollmentModel
from app.model.lesson_score import LessonScoreModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class LessonRepository:

    def get(self, uuid: str, session=None) -> LessonModel:
        logger.info("Get CourseRepository")
        lesson = session.query(LessonModel).get(uuid)

        return lesson

    def get_all_active_with_user_lessons(self, course_id, session=None):
        logger.info("get_all_active CourseRepository")
        ids = []
        lesson_scores = session.query(LessonScoreModel.lesson_id)\
            .filter(LessonScoreModel.enrollment_id == EnrollmentModel.id)\
            .filter(EnrollmentModel.course_id == course_id)\
            .all()
        if lesson_scores is not None:
            ids = [lesson_id for lesson_id, in lesson_scores]
        print(ids)
        lessons = session.query(LessonModel).filter(LessonModel.active).order_by(LessonModel.order).all()
        return lessons, ids

    def get_all_active(self, course_id, session=None):
        logger.info("get_all_active CourseRepository")
        lessons = session.query(LessonModel).filter(LessonModel.course_id == course_id, LessonModel.active).all()
        return lessons

    def get_all_not_in(self, lessons_id, session=None):
        logger.info("get_all_not_in get_all_not_in")
        lessons = session.query(LessonModel).filter(LessonModel.id.notin_(lessons_id), LessonModel.active).all()
        return lessons

    def save(self, data: Dict, course_id: str, user_id: str, session=None) -> LessonModel:
        try:
            logger.info("save LessonRepository")
            lessons_count = session.query(LessonModel.course_id).filter(LessonModel.course_id == course_id).count()
            lesson = LessonModel()

            lesson.name = data['name']
            lesson.description = data['description']
            lesson.code = data['code']
            lesson.description = data['description']
            lesson.question_details = data['question_details']
            lesson.code = data.get('code', '')
            lesson.hours = data.get('hours', 0)
            lesson.score = data['score']
            lesson.aproval_score = data['aproval_score']
            lesson.course_id = course_id
            lesson.created_by = user_id
            lesson.updated_by = user_id
            lesson.active = True
            lesson.order = lessons_count + 1

            session.add(lesson)
            session.commit()
            return lesson
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("Something is bad in your request.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

