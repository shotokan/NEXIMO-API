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


class LessonScoreRepository:

    def get(self, uuid: str, session=None) -> LessonModel:
        logger.info("Get EnrollmentRepository")
        lesson = session.query(LessonScoreModel).get(uuid)

        return lesson

    def get_lesson_by_user(self, lesson_id, user_id, session=None):
        logger.info("get_all_active EnrollmentRepository")
        lessons_taken = session.query(LessonScoreModel)\
            .filter(LessonScoreModel.lesson_id == lesson_id, LessonModel.active).first()
        return lessons_taken
